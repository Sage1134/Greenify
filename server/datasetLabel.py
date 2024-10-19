import os

imageFolder = "server/WasteDataset/Images"
labelFolder = "server/WasteDataset/Labels"

classes = {
    "DisposableContainers": 0,
    "Hersheys": 1,
    "Nestle": 2,
    "Pepsi": 3,
    "PlasticBags": 4,
    "PlasticStraws": 5,
    "PlasticUtensils": 6,
    "RedMeats": 7,
}

os.makedirs(labelFolder, exist_ok=True)

def createLabel(class_id):
    center_x = 0.5
    center_y = 0.5
    width = 1.0
    height = 1.0
    label = f"{class_id} {center_x} {center_y} {width} {height}\n"
    return label

for class_name, class_id in classes.items():
    class_folder = os.path.join(imageFolder, class_name)
    if os.path.exists(class_folder):
        for imgFile in os.listdir(class_folder):
            if imgFile.endswith(".jpg") or imgFile.endswith(".png"):
                label = createLabel(class_id)
                label_filename = os.path.join(labelFolder, imgFile.replace(".jpg", ".txt").replace(".png", ".txt"))
                with open(label_filename, "w") as f:
                    f.write(label)
                print(f"Label saved for {imgFile}: {label.strip()}")
    else:
        print(f"Class folder {class_name} does not exist.")
