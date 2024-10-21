from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import json
from ultralytics import YOLO
from flask_cors import CORS
import os

model = YOLO("yolov8n.pt")

def loadAdvice(adviceFile):
    with open(adviceFile, 'r') as f:
        return json.load(f)

def detectClasses(imagePath, adviceFile):
    results = model.predict(source=imagePath, conf=0.5)

    detectedClasses = set()
    adviceDict = loadAdvice(adviceFile)

    targetClasses = [
        "bottle",
        "cup",
        "fork",
        "knife",
        "spoon",
        "hot dog",
        "microwave",
        "oven",
        "toaster"
    ]

    for result in results:
        classIndices = result.boxes.cls.int().tolist()
        classNames = [result.names[i] for i in classIndices]
        filteredClasses = [name for name in classNames if name in targetClasses]
        detectedClasses.update(filteredClasses)

    adviceList = [adviceDict[cls] for cls in detectedClasses if cls in adviceDict]

    return [list(detectedClasses), adviceList]

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'server'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/process_frame", methods=['POST'])
def process_frame():
    try:
        if 'image' not in request.files:
            app.logger.error('No file part in the request')
            return 'No file part', 400
        file = request.files['image']
        if file.filename == '':
            app.logger.error('No selected file')
            return 'No selected file', 400
        file_path = os.path.join(UPLOAD_FOLDER, 'capture.png')
        file.save(file_path)
        
        detectedClasses, adviceList = detectClasses(file_path, "advice.json")
        
        app.logger.info(f'File successfully saved to {file_path}')
        
        print(detectedClasses, adviceList)
        return jsonify({
            'detected_classes': detectedClasses,
            'advice': adviceList
        }), 200
        
    except Exception as e:
        app.logger.error(f'Error processing file: {e}')
        return jsonify({'message': 'Error processing file'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)