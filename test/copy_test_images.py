import os
import pandas as pd
import shutil

df = pd.read_csv("../data/labels_fixed.csv")
df = df[df['angle'] != 'not_car']
df = df[df['split']=='test']

test_list = df['image_id'].to_list()

source_folder = "../data/raw"
destination_folder = "./test_images"

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for image_id in test_list:
    image_name = f"{image_id:06d}.jpg"
    source_path = os.path.join(source_folder, image_name)
    destination_path = os.path.join(destination_folder, image_name)

    if os.path.exists(source_path):
        shutil.copy2(source_path, destination_path)
        print(f"Successfully copied: {image_name}")
    else:
        print(f"Warning: {image_name} not found in {source_folder}")