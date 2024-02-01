from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def upload_image_to_imgbb(image_path):
    api_key = '8602358fc27d0309cd2637c8e965dbe3' 
    api_url = 'https://api.imgbb.com/1/upload'

    with open(image_path, 'rb') as file:
        files = {'image': (image_path, file)}
        params = {'key': api_key}
        try:
            response = requests.post(api_url, params=params, files=files)
            response.raise_for_status()  # Mengangkat pengecualian jika respons status bukan 2xx
            result_url = response.json()['data']['url']
            return result_url
        except requests.exceptions.RequestException as e:
            print(f"Error during ImgBB upload: {e}")
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
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
        return "Gagal mengonversi gambar ke URL. Cek log server untuk detail kesalahan."

@app.route('/result')
def result():
    return "Silakan unggah gambar terlebih dahulu."

if __name__ == '__main__':
    app.run(debug=True)
