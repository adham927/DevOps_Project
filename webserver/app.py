import requests
from flask import Flask, send_file, request, render_template
import boto3

app = Flask(__name__, static_url_path='')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def hello_world():
    data = request.data
    prediction = requests.get(f'http://mnist-predictor-service:8080/predict', data=data)
    s3_client = boto3.client('s3')
    s3_client.upload_file(data, 'adhambucket1', 'adham/my_image')
    return prediction.json()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8081)


