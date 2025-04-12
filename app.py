import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

app = Flask(__name__)

# 업로드 및 변환된 이미지 저장 폴더
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'static/converted'

# 폴더 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# PDF 변환 설정
POPPLER_PATH = r"C:\Users\user\Downloads\poppler-24.08.0\Library\bin"  # 윈도우 사용자는 여기에 poppler 경로 지정 필요

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
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # PDF -> 이미지로 변환
        try:
            images = convert_from_path(filepath, poppler_path=POPPLER_PATH)
        except Exception as e:
            return f"PDF 변환 실패: {e}"

        image_urls = []
        base_filename = os.path.splitext(filename)[0]
        for i, image in enumerate(images):
            image_filename = f"{base_filename}_{i + 1}.jpg"
            image_path = os.path.join(CONVERTED_FOLDER, image_filename)
            image.save(image_path, 'JPEG')
            image_urls.append(url_for('static', filename=f"converted/{image_filename}"))

        return render_template('index.html', image_urls=image_urls)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
