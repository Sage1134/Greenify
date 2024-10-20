from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import json
from ultralytics import YOLO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "This is actually so freaking cool lmao",
        'people': ["yang", "name", "another name"]
    })

@app.route("/api/process_frame", methods=['POST'])
def process_frame():
    data = request.json
    image_data = data['image'].split(',')[1]
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # do the logic for adding keypoints to the body
    _, buffer = cv2.imencode('.png', img)
    response_image = base64.b64encode(buffer).decode('utf-8')
    return jsonify({'processed_image': response_image})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
