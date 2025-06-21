from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from PIL import Image
import pytesseract

# Set the path to your Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ''
    if request.method == 'POST':
        file = request.files['document']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            image = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(image)

    return render_template('index.html', text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
