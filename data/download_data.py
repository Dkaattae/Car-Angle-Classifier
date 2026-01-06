import os
import io
import csv
import requests
from PIL import Image
from ddgs import DDGS
from itertools import count

DATA_DIR = './'
CSV_PATH = "labels.csv"
fieldnames = ["image_id", "split", "angle", "make", "model", "width", "height"]
# Image parameters
MIN_SIZE = 250
MAX_SIZE = 1024
JPEG_QUALITY = 85
image_counter = count(start=1700)

def next_image_id():
    return f"{next(image_counter):06d}"

def init_csv():
    file_exists = os.path.isfile(CSV_PATH)
    csv_file = open(CSV_PATH, "a", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    return csv_file, writer

def save_image_proportional(img, save_path):
    # Skip tiny images
    if img.width < MIN_SIZE or img.height < MIN_SIZE:
        return False

    # Resize proportionally if too big
    if max(img.width, img.height) > MAX_SIZE:
        scale = MAX_SIZE / max(img.width, img.height)
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)

    # Save as JPEG compressed
    img.save(save_path, format="JPEG", quality=JPEG_QUALITY)
    return img.width, img.height

def download_duckduckgo_images(query, split, angle, max_images=100):
    save_dir = os.path.join(DATA_DIR, split)
    os.makedirs(save_dir, exist_ok=True)
    csv_file, writer = init_csv()

    with DDGS() as ddgs:
        results = ddgs.images(query, safesearch="moderate", type_image="photo", max_results=max_images)
        for r in results:
            image_id = next_image_id()
            filename = f"{image_id}.jpg"
            filepath = os.path.join(save_dir, filename)

            try:
                img_bytes = requests.get(r["image"], timeout=10).content
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                size = save_image_proportional(img, filepath)
                if not size:
                    continue 

                width, height = size
                writer.writerow({
                    "image_id": image_id,
                    "split": split,
                    "angle": angle,
                    "make": "",
                    "model": "",
                    "width": width,
                    "height": height
                })

            except Exception as e:
                print(f"Error downloading or processing image: {e}")
                continue

    csv_file.close()
    return image_id

if __name__ == "__main__":
    angle_list = [
        # "front", 
        # "side", 
        "rear"]
    # setting_list = ["street", "night", "day", "highway", "parking lot"]
    query_list = [
        # 'car "front view" -people -interior', 
        # 'car "side profile" white background', 
        'Full car rear profile'
    ]
    query_map = dict(zip(angle_list, query_list))
    for angle in angle_list:
        query = query_map[angle]
        image_id = download_duckduckgo_images(
            query=query,
            split="dealer",
            angle=angle
        )
    print("angle: ", angle, ", image_id: ", image_id)
