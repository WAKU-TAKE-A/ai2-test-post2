#-*-coding:utf-8;-*-

import base64
from flask import Flask, request
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/post',methods=["POST"])
def test_post():
    print(request.headers)
    str_enc = request.json['image']
    bin_dec = base64.urlsafe_b64decode(
        str_enc + '=' * (-len(str_enc) % 4))
    fnm = 'C:/tmp/flsk-test-post/tmp000.jpg'
    with open(fnm, "wb") as f:
        f.write(bin_dec)
    return '{"json":{"image":"' + str_enc + '"}}'

@app.route('/blur',methods=["POST"])
def test_blur():
    print('OpenCV version is {0}'.format(cv2.__version__))
    size = request.args.get('size', default=3, type=int)
    str_enc = request.json['image']
    bin_dec = base64.urlsafe_b64decode(
        str_enc + '=' * (-len(str_enc) % 4))
    nparr = np.fromstring(bin_dec, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_blur = cv2.blur(img, (size, size))
    ret, img_enc = cv2.imencode('.jpg', img_blur)
    str_enc_blur = base64.b64encode(img_enc).decode('utf-8')
    return '{"json":{"image":"' + str_enc_blur + '"}}'
