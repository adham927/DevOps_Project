import requests
from flask import Flask, send_file, request, render_template
import boto3
import re
import base64
from PIL import Image
import io
from datetime import datetime



app = Flask(__name__, static_url_path='')
date = datetime.now().strftime("%I:%M:%S")

@app.route("/")
def home():
    return render_template('index.html')

def getI420FromBase64(codec):
    base64_data = re.sub('^data:image/.+;base64,', '', codec.decode())
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    img.load()  # required for png.split()
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
    background.save('image.jpg', 'JPEG', quality=80)
    img.save('image.png', "PNG")

@app.route("/upload", methods=['POST'])
def hello_world():
    data = request.data
    s3_client = boto3.client('s3')
    getI420FromBase64(data)
    s3_client.upload_file(f'image{date}.png', 'adhambucket1', f'image{date}.png')
    prediction = requests.get(f'http://mnist-predictor-service:8080/predict', data=data)
    return prediction.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)