from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def upload_image_to_imgbb(image_path):
    api_key = '8602358fc27d0309cd2637c8e965dbe3'  # Ganti dengan API key ImgBB Anda
    api_url = 'https://api.imgbb.com/1/upload'

    with open(image_path, 'rb') as file:
        files = {'image': (image_path, file)}
        params = {'key': api_key}
        response = requests.post(api_url, params=params, files=files)

    if response.status_code == 200:
        result_url = response.json()['data']['url']
        return result_url
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    image_path = f"uploads/{file.filename}"
    file.save(image_path)

    imgbb_url = upload_image_to_imgbb(image_path)

    if imgbb_url:
        return render_template('result.html', img_url=imgbb_url)
    else:
        return "Gagal mengonversi gambar ke URL."

@app.route('/result')
def result():
    return "Silakan unggah gambar terlebih dahulu."

if __name__ == '__main__':
    app.run(debug=True)
