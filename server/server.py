from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import json
from ultralytics import YOLO
from flask_cors import CORS

# Load the YOLO model
model = YOLO("yolov8n.pt")

# Function to load advice from a JSON file
def loadAdvice(adviceFile):
    with open(adviceFile, 'r') as f:
        return json.load(f)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Allow CORS for requests from localhost:3000

# Endpoint for the home route
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "This is actually so freaking cool lmao",
        'people': ["yang", "name", "another name"]
    })

# Endpoint to process the frame from the frontend
@app.route("/api/process_frame", methods=['POST'])
def process_frame():
    data = request.json
    image_data = data['image'].split(',')[1]  # Get the image data from the request
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)  # Decode the base64 image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Convert it to an OpenCV image

    # Perform detection and get advice
    detected_classes, advice_list = detectClasses(img, "advice.json")

    # Return the advice in the specified format
    return jsonify({'advice': [detected_classes, advice_list]})

# Function to detect classes in the image and retrieve advice
def detectClasses(img, adviceFile):
    results = model.predict(source=img, conf=0.5)  # Adjust confidence threshold as needed
    detected_classes = set()
    advice_dict = loadAdvice(adviceFile)

    # Define target classes you are interested in
    target_classes = [
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
        class_indices = result.boxes.cls.int().tolist()  # Get class indices
        class_names = [result.names[i] for i in class_indices]  # Get class names from indices

        # Filter detected classes based on target classes
        filtered_classes = [name for name in class_names if name in target_classes]
        detected_classes.update(filtered_classes)

    # Retrieve advice for detected classes
    advice_list = [advice_dict[cls] for cls in detected_classes if cls in advice_dict]

    return list(detected_classes), advice_list

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # Run the Flask app
