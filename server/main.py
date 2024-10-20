import json
from ultralytics import YOLO

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

detectedClasses = detectClasses("./test.jpg", "./advice.json")
print(detectedClasses)
