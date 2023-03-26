import logging
import os.path

from app.converter import converter
from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename

# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%bot %H:%M:%S',
                    level=logging.INFO)
# logging config]

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'templates/static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.secret_key = "some_secret_key"

UPLOAD_FOLDER = os.path.join(project_root, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'.docx', '.pdf', '.doc', '.jpg', '.jpeg', '.gif', '.png', '.bmp', '.svg', '.tiff',
                                    '.htm', '.html', '.docm', '.dotx', '.dot', '.md', '.rtf', '.odt', '.ott', '.txt',
                                    '.mobi', '.mht', '.mhtml', '.xht', '.xhtml', '.chm', '.zip', '.rar', '.7z', '.tar',
                                    '.tar.gz', '.wps', '.wpt'}
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024


# http://localhost:5000
@app.route('/', methods=['GET'])
def index():
    logging.info('Showing index page')
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_files():
    """Upload a file."""
    logging.info('Starting file upload')

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    new_file_extension = request.form.get('saveAs')

    # obtaining the name of the destination file
    filename = file.filename
    if filename == '':
        logging.info('Invalid file')
        flash('No file selected for uploading')
        return redirect(request.url)
    else:
        logging.info('Selected file is= [%s]', filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext in app.config['ALLOWED_EXTENSIONS']:
            secure_file_name = secure_filename(filename)
            file_path = os.path.join(UPLOAD_FOLDER, secure_file_name)

            file.save(file_path)
            logging.info('Upload is successful')
            flash('File uploaded successfully')

            converter(file_path, new_file_extension)
            logging.info('Conversion is successful')
            flash('Conversion ran successfully')
            return redirect('/')
        else:
            logging.info('Invalid file extension')
            flash('Not allowed file type')
            return redirect(request.url)


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a file."""
    logging.info('Downloading file= [%s]', filename)
    logging.info(app.root_path)
    full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
    logging.info(full_path)
    return send_from_directory(full_path, filename, as_attachment=True)


# http://localhost:5000/files
@app.route('/files', methods=['GET'])
def list_files():
    """Endpoint to list files."""
    logging.info('Listing already uploaded files from the upload folder.')
    upf = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            upf.append(filename)

    # return jsonify(uploaded_files)
    return render_template('list.html', files=upf)


def check_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)


if __name__ == '__main__':
    check_upload_dir()
    # Development only: run "python app.py" and open http://localhost:5000
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=False, port=server_port, host='0.0.0.0')
