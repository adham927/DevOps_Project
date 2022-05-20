import requests
from flask import Flask, send_file, request, render_template
import boto3
import re
import base64
from PIL import Image
import io
import datetime
from loguru import logger

app = Flask(__name__, static_url_path='')


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
    img.save('img.png', "PNG")

@app.route("/upload", methods=['POST'])
def hello_world():
    logger.debug("datetime set")
    data = request.data
    getI420FromBase64(data)
    s3_client = boto3.client('s3')
    s3_client.upload_file('img.png', 'adhambucket1', f'image_{datetime.datetime.now().second}.png')
    logger.debug("image uploaded to s3")
    prediction = requests.get(f'http://mnist-predictor-service:8080/predict', data=data)
    return prediction.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)