import zipfile
import os
import time
import uuid
import hashlib
import json

# Paths (customized for your setup)
BASE_DIR = r"C:\Users\acer\Desktop\VaultFile"
FOLDER_TO_ZIP = os.path.join(BASE_DIR, "my_data")
TEMP_ZIP = os.path.join(BASE_DIR, "data.zip")
OUTPUT_FILE = os.path.join(BASE_DIR, "vault.qvault")

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"[+] Folder zipped as {zip_path}")

def make_header(data_file):
    with open(data_file, 'rb') as f:
        data = f.read()
        data_hash = hashlib.sha256(data).hexdigest()

    header = {
        "magic": "QVAULT",
        "version": 1,
        "timestamp": int(time.time()),
        "block_id": str(uuid.uuid4()),
        "data_hash": data_hash,
        "encryption": "pending_kyber1024"
    }
    return header

def create_qvault(header, data_file, output_file):
    with open(output_file, 'wb') as out:
        header_bytes = json.dumps(header).encode('utf-8')
        out.write(len(header_bytes).to_bytes(4, 'big'))  # Write header size first
        out.write(header_bytes)

        with open(data_file, 'rb') as f:
            out.write(f.read())
    
    print(f"[+] .qvault file created: {output_file}")

# -------- MAIN --------
if __name__ == "__main__":
    zip_folder(FOLDER_TO_ZIP, TEMP_ZIP)
    header = make_header(TEMP_ZIP)
    create_qvault(header, TEMP_ZIP, OUTPUT_FILE)

    # Cleanup
    os.remove(TEMP_ZIP)
    print("[*] Temp zip deleted. Vault ready.")
