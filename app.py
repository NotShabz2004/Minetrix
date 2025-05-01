from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
import os
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

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

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/index')
def main_page():
    return render_template('index.html')

@app.route('/encryption', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    filename = file.filename
    file_path = os.path.join('uploads', filename)
    output_path = os.path.join('encrypted', filename + '.enc')

    os.makedirs('uploads', exist_ok=True)
    os.makedirs('encrypted', exist_ok=True)

    file.save(file_path)
    encrypt_file(file_path, filename, output_path, KEY)

    # Save filename in session to access in next route
    session['encrypted_filename'] = filename + '.enc'
    return render_template('loading.html')

@app.route('/encryption-complete')
def encryption_complete():
    filename = session.get('encrypted_filename')
    if not filename:
        return redirect(url_for('index'))
    return render_template('encryption.html', filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory('encrypted', filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
