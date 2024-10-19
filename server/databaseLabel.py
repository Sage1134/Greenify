import os
import shutil
import random

imageFolder = "server/WasteDataset/Images"
labelFolder = "server/WasteDataset/Labels"
trainFolder = os.path.join(imageFolder, "Train")
valFolder = os.path.join(imageFolder, "Val")
trainLabelFolder = os.path.join(labelFolder, "Train")
valLabelFolder = os.path.join(labelFolder, "Val")

os.makedirs(trainFolder, exist_ok=True)
os.makedirs(valFolder, exist_ok=True)
os.makedirs(trainLabelFolder, exist_ok=True)
os.makedirs(valLabelFolder, exist_ok=True)

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

def createLabel(class_id):
    center_x = 0.5
    center_y = 0.5
    width = 1.0
    height = 1.0
    label = f"{class_id} {center_x} {center_y} {width} {height}\n"
    return label

val_split_probability = 0.2

train_image_counter = 0
val_image_counter = 0

for class_name, class_id in classes.items():
    class_folder = os.path.join(imageFolder, class_name)
    
    if os.path.exists(class_folder):
        img_files = [img for img in os.listdir(class_folder) if img.endswith((".jpg", ".png"))]
        random.shuffle(img_files)
        
        for imgFile in img_files:
            if random.random() < val_split_probability:
                
                new_img_name = f"image{val_image_counter}.png"
                shutil.copy(os.path.join(class_folder, imgFile), os.path.join(valFolder, new_img_name))
                
                label = createLabel(class_id)
                label_filename = os.path.join(valLabelFolder, new_img_name.replace(".png", ".txt"))
                with open(label_filename, "w") as f:
                    f.write(label)
                    
                print(f"Val Label saved for {new_img_name}: {label.strip()}")
                val_image_counter += 1
            else:
                new_img_name = f"image{train_image_counter}.png"
                shutil.copy(os.path.join(class_folder, imgFile), os.path.join(trainFolder, new_img_name))
                
                label = createLabel(class_id)
                label_filename = os.path.join(trainLabelFolder, new_img_name.replace(".png", ".txt"))
                with open(label_filename, "w") as f:
                    f.write(label)
                    
                print(f"Train Label saved for {new_img_name}: {label.strip()}")
                train_image_counter += 1
    else:
        print(f"Class folder {class_name} does not exist.")

print("Dataset splitting completed.")
