import os
import csv
import numpy as np
import onnxruntime as ort
from io import BytesIO
from urllib import request
import base64
import json
from PIL import Image

onnx_model_path = os.getenv("MODEL_PATH", "car_angle_classifier.onnx")

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_pytorch_style(X):
    # X: shape (1, 299, 299, 3), dtype=float32, values in [0, 255]
    X = X / 255.0

    mean = np.array([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    # Convert NHWC → NCHW
    # from (batch, height, width, channels) → (batch, channels, height, width)
    X = X.transpose(0, 3, 1, 2)  

    # Normalize
    X = (X - mean) / std

    return X.astype(np.float32)

def get_s3_test_list():
    csv_path = 'labels_fixed.csv'
    valid_files = set()
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                split = row['split']
                angle = row['angle']
                if split == 'test' and angle != 'not_car':
                    image_id = row['image_id']
                    filename = f"{int(image_id):06d}.jpg"
                    valid_files.add(filename)
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return valid_files

def get_image(body):

    if "image_data" in body:
        image_bytes = base64.b64decode(body["image_data"])
        img = Image.open(BytesIO(image_bytes))
    elif "url" in body:
        img = download_image(body["url"])
    elif body.get("source") == "s3":
        bucket = body.get('bucket').strip()
        key = body.get('key').strip()
        test_list = get_s3_test_list()
        if key not in test_list:
            print(key, test_list[0])
            raise ValueError("image not found in s3")
        import boto3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        image_bytes = response['Body'].read()
        img = Image.open(BytesIO(image_bytes))
    else:
        raise ValueError("unsupported image source")
    return img

def predict(img, onnx_model_path):
    input_size = 224
    
    img = prepare_image(img, (input_size,input_size))

    X = np.array(img)
    X = np.expand_dims(X, axis=0)
    input_array = preprocess_pytorch_style(X)

    session = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

    inputs = session.get_inputs()
    outputs = session.get_outputs()

    input_name = inputs[0].name
    output_name = outputs[0].name

    results = session.run([output_name], {input_name: input_array})

    label_list = ['front', 'rear', 'side']

    predictions = results[0][0].tolist()

    return dict(zip(label_list, predictions))


def lambda_handler(event, context):
    if "body" in event and event["body"]:
        if event.get('isBase64Encoded'):
            body_str = event.get('body', '{}')
            body = base64.b64decode(body_str).decode('utf-8')
        else:
            body = json.loads(event["body"])
    else:
        body = event
    print(body)
    try: 
        img = get_image(body)
    except ValueError as e:
        print(f"unexpected Error: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}
    predictions = predict(img, onnx_model_path)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(predictions)
    }
