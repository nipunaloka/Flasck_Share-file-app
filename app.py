from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure app settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB file size limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = 'your_secret_key'  # For flash messages

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route with upload form
@app.route('/')
def upload_form():
    # Get the list of uploaded files (including previous uploads)
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    return render_template('upload.html', uploaded_files=uploaded_files)

# Handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part in the request')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('File uploaded successfully!')
        return redirect(url_for('upload_form'))

    flash('Invalid file type. Allowed types: png, jpg, jpeg, gif, pdf, txt, docx')
    return redirect(request.url)

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handler for large files
@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File is too large. Maximum allowed size is 16 MB.')
    return redirect(url_for('upload_form'))

if __name__ == '__main__':
    app.run(debug=True)
