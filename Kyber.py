import os
import oqs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def generate_kyber_keys(pub_key_path, priv_key_path):
    with oqs.KeyEncapsulation('Kyber1024') as kem:
        public_key = kem.generate_keypair()
        with open(pub_key_path, 'wb') as f:
            f.write(public_key)
        with open(priv_key_path, 'wb') as f:
            f.write(kem.export_secret_key())

def encapsulate_key(pub_key_path, ct_path):
    with open(pub_key_path, 'rb') as f:
        public_key = f.read()
    with oqs.KeyEncapsulation('Kyber1024') as kem:
        kem.import_public_key(public_key)
        ciphertext, shared_secret = kem.encap_secret()
    with open(ct_path, 'wb') as f:
        f.write(ciphertext)
    return shared_secret

def decapsulate_key(priv_key_path, ct_path):
    with open(priv_key_path, 'rb') as f:
        secret_key = f.read()
    with open(ct_path, 'rb') as f:
        ciphertext = f.read()
    with oqs.KeyEncapsulation('Kyber1024') as kem:
        kem.import_secret_key(secret_key)
        shared_secret = kem.decap_secret(ciphertext)
    return shared_secret

def encrypt_file(file_path, output_path, shared_key):
    with open(file_path, "rb") as f:
        data = f.read()
    iv = get_random_bytes(16)
    cipher = AES.new(shared_key[:32], AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)

def decrypt_file(file_path, output_path, shared_key):
    with open(file_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(shared_key[:32], AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    with open(output_path, "wb") as f:
        f.write(plaintext)

def encrypt_directory(input_dir, output_dir, pub_key_path, ct_path):
    shared_key = encapsulate_key(pub_key_path, ct_path)
    for root, _, files in os.walk(input_dir):
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, input_dir)
            enc_name = rel_path.replace(os.sep, "__") + ".enc"
            enc_path = os.path.join(output_dir, enc_name)
            os.makedirs(os.path.dirname(enc_path), exist_ok=True)
            encrypt_file(full_path, enc_path, shared_key)
            print(f"Encrypted: {rel_path}")

def decrypt_directory(input_dir, output_dir, priv_key_path, ct_path):
    shared_key = decapsulate_key(priv_key_path, ct_path)
    for root, _, files in os.walk(input_dir):
        for name in files:
            if name.endswith(".enc"):
                full_path = os.path.join(root, name)
                rel_path = os.path.relpath(full_path, input_dir)
                original_name = rel_path.replace("__", os.sep)[:-4]
                output_path = os.path.join(output_dir, original_name)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                decrypt_file(full_path, output_path, shared_key)
                print(f"Decrypted: {rel_path}")

# ========== MENU ==========
while True:
    print("\n========= Kyber1024 + AES Hybrid File Encrypter =========")
    print("1. Generate Kyber Key Pair")
    print("2. Encrypt Folder")
    print("3. Decrypt Folder")
    print("4. Exit")
    option = input("Enter Option: ").strip()

    if option == '1':
        pub = input("Enter public key filename (e.g., pub.key): ").strip()
        priv = input("Enter private key filename (e.g., priv.key): ").strip()
        generate_kyber_keys(pub, priv)
        print("Key pair generated.")

    elif option == '2':
        rawPath = input("Enter Raw Folder Path: ").strip()
        encPath = input("Enter Encrypted Output Folder Path: ").strip()
        pubKey = input("Enter Public Key File: ").strip()
        ctFile = input("Enter File to Store Encapsulated Key (e.g., ct.bin): ").strip()
        encrypt_directory(rawPath, encPath, pubKey, ctFile)

    elif option == '3':
        encPath = input("Enter Encrypted Folder Path: ").strip()
        decPath = input("Enter Decrypted Output Folder Path: ").strip()
        privKey = input("Enter Private Key File: ").strip()
        ctFile = input("Enter File Containing Encapsulated Key (e.g., ct.bin): ").strip()
        decrypt_directory(encPath, decPath, privKey, ctFile)

    elif option == '4':
        print("EXITING.")
        break

    else:
        print("Invalid option. Try again.")
