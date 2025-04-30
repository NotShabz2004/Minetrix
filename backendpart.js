document.addEventListener('DOMContentLoaded', function() {
  const uploadBtn = document.getElementById('uploadBtn');
  const fileInput = document.getElementById('fileInput');
  const fileDetails = document.getElementById('fileDetails');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const encryptBtn = document.getElementById('encryptBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const decryptBtn = document.getElementById('decryptBtn');
  const trespasserInfo = document.getElementById('trespasserInfo');
  const encryptedData = document.getElementById('encryptedData');

  fileDetails.style.display = 'none';
  encryptedData.style.display = 'none';

  uploadBtn.addEventListener('click', function() {
    fileInput.click();
  });

  fileInput.addEventListener('change', function(e) {
    if (e.target.files.length) {
      const file = e.target.files[0];
      fileName.textContent = file.name;
      fileSize.textContent = formatFileSize(file.size);
      fileDetails.style.display = 'block';
      fileDetails.querySelector('.status').classList.add('active');
      encryptBtn.disabled = false;
    }
  });

  encryptBtn.addEventListener('click', function() {
    encryptBtn.textContent = 'Encrypting...';
    encryptBtn.disabled = true;
    
    setTimeout(() => {
      trespasserInfo.innerHTML = '<p><span class="status active"></span> Encrypted data available</p>';
      encryptedData.style.display = 'block';
      decryptBtn.disabled = false;
      downloadBtn.disabled = false;
      encryptBtn.textContent = 'Encrypt & Store';
      encryptBtn.disabled = false;
    }, 1000);
  });

  downloadBtn.addEventListener('click', function() {
    alert('File download would be triggered here');
  });

  decryptBtn.addEventListener('click', function() {
    alert('Decryption attempt would be made here');
  });

  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
});