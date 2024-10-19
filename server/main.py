from ultralytics import YOLO
model = YOLO("yolov8n.pt")

def detect_classes(image_path):
    results = model.predict(source=image_path, conf=0.5)

    detected_classes = set()

    for result in results:
        class_indices = result.boxes.cls.int().tolist()
        class_names = [result.names[i] for i in class_indices]

        detected_classes.update(class_names)

    return list(detected_classes)


detected_classes = detect_classes("server/WasteDataset/Images/Train/image81.png")
print(detected_classes)