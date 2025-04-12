import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 업로드 폴더 설정
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return redirect(request.url)

    file = request.files['pdfFile']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_url = url_for('static', filename=f'uploads/{filename}')
        return render_template('index.html', file_url=file_url)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
