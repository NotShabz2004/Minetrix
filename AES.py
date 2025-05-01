import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

KEY = get_random_bytes(32)

def encrypt_file(file_path, rel_path, output_path, ENC_KEY):
    with open(file_path, "rb") as f:
        data = f.read()

    rel_path_bytes = rel_path.encode()
    path_len = len(rel_path_bytes).to_bytes(2, 'big')

    iv = get_random_bytes(16)
    cipher = AES.new(ENC_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(path_len + rel_path_bytes + data, AES.block_size))

    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)

def decrypt_file(file_path, output_dir, DEC_KEY):
    with open(file_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(DEC_KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    path_len = int.from_bytes(plaintext[:2], 'big')
    rel_path = plaintext[2:2 + path_len].decode()
    original_data = plaintext[2 + path_len:]

    output_path = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(original_data)

def encrypt_directory(input_dir, output_dir, KEY_PATH):
    with open(KEY_PATH, "wb") as f:
        f.write(KEY)

    for root, _, files in os.walk(input_dir):
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, input_dir)

            encrypted_name = rel_path.replace(os.sep, "_") + ".enc"
            encrypted_path = os.path.join(output_dir, encrypted_name)

            os.makedirs(os.path.dirname(encrypted_path), exist_ok=True)
            encrypt_file(full_path, rel_path, encrypted_path, KEY)

            print(f"Encrypted: {rel_path}")

def decrypt_directory(input_dir, output_dir, KEY_PATH):
    with open(KEY_PATH, "rb") as f:
        DEC_KEY = f.read()

    for root, _, files in os.walk(input_dir):
        for name in files:
            if name.endswith(".enc"):
                full_path = os.path.join(root, name)
                decrypt_file(full_path, output_dir, DEC_KEY)

                print(f"Decrypted: {name}")

# === Menu ===
while True:
    print("============= AES Encrypter =============")
    print("1. Encrypt Directory")
    print("2. Decrypt Directory")
    print("3. Exit")
    option = input("Enter Option: ").strip()

    print("=========================================")

    if option == "1":
        rawPath = input("Enter Folder to Encrypt: ").strip()
        encPath = input("Enter Destination Folder for Encrypted Files: ").strip()
        key = input("Enter Key filename (e.g., aes.key): ").strip()

        encrypt_directory(rawPath, encPath, key)

    elif option == "2":
        encPath = input("Enter Folder with Encrypted Files: ").strip()
        decPath = input("Enter Destination Folder to Decrypt: ").strip()
        key = input("Enter Key filename (e.g., aes.key): ").strip()

        decrypt_directory(encPath, decPath, key)

    elif option == "3":
        print("EXIT")
        break

    else:
        print("Invalid Input. Try again.")
