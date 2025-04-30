#Test this code with NewFolder

import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

KEY = get_random_bytes(32)

def encrypt_file(file_path, output_path, ENC_KEY):
    with open(file_path, "rb") as f:
        data = f.read()

    file_name = os.path.basename(file_path).encode()
    name_len = len(file_name).to_bytes(2, 'big')

    iv = get_random_bytes(16)
    cipher = AES.new(ENC_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(name_len + file_name + data, AES.block_size))

    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)


def decrypt_file(file_path, output_dir, DEC_KEY):
    with open(file_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(DEC_KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    name_len = int.from_bytes(plaintext[:2], 'big')
    original_name = plaintext[2:2 + name_len].decode()
    original_data = plaintext[2 + name_len:]

    output_path = os.path.join(output_dir, original_name)
    os.makedirs(os.path.dirname(output_path), exist_ok = True)

    with open(output_path, "wb") as f:
        f.write(original_data)

def encrypt_directory(input_dir, output_dir, KEY_PATH):

    with open(KEY_PATH, "wb") as f:
        f.write(KEY)

    for root, _, files in os.walk(input_dir):

        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, input_dir)

            encrypted_name = rel_path.replace(os.sep, "__") + ".enc"
            encrypted_path = os.path.join(output_dir, encrypted_name)

            os.makedirs(os.path.dirname(encrypted_path), exist_ok=True)
            encrypt_file(full_path, encrypted_path, KEY)

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


while True:
    print("============= AES Encrypter =============")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")
    option = int(input("Enter Option: "))

    print("=========================================")

    if option == 1:
        rawPath = input("Enter Raw File Path: ")
        encPath = input("Enter Encrypted File name (end with .enc): ")
        key = input("Enter Key (end with .key): ")

        encrypt_directory(rawPath, encPath, key)
    
    elif option == 2:
        encPath = input("Enter Encrypted File name (end with .enc): ")
        decPath = input("Enter Raw File Path: ")
        key = input("Enter Key (end with .key): ")

        decrypt_directory(encPath, decPath, key)
    
    elif option == 3:
        print("EXIT")
        break

    else:
        print("Invalid Input")
        break
