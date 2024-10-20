from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import json
from ultralytics import YOLO
from flask_cors import CORS

model = YOLO("yolov8n.pt")

def loadAdvice(adviceFile):
    with open(adviceFile, 'r') as f:
        return json.load(f)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'server'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

detectedClasses = detectClasses("server/test.jpg", "advice.json")
print(detectedClasses)
