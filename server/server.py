from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import json
from ultralytics import YOLO
from flask_cors import CORS

# Load the YOLO model
model = YOLO("yolov8n.pt")

def loadAdvice(adviceFile):
    """Load advice from a JSON file."""
    with open(adviceFile, 'r') as f:
        return json.load(f)

def detectClasses(image, adviceFile):
    """Detect specified classes in the image and return detected classes and their corresponding advice."""
    results = model.predict(source=image, conf=0.5)  # You can adjust the confidence threshold here

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
        classIndices = result.boxes.cls.int().tolist()  # Convert tensor to list of class indices
        classNames = [result.names[i] for i in classIndices]  # Get class names from indices
        filteredClasses = [name for name in classNames if name in targetClasses]
        detectedClasses.update(filteredClasses)

    # Collect advice for detected items
    adviceList = [adviceDict[cls] for cls in detectedClasses if cls in adviceDict]

    return list(detectedClasses), adviceList

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
    image_data = data['image'].split(',')[1]  # Get the base64 image string
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decode the image
    
    # Detect classes and retrieve advice
    detectedClasses, adviceList = detectClasses(img, 'advice.json')

    return jsonify({
        'detected_classes': detectedClasses,
        'advice': adviceList
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
