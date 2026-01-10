import requests
import base64
from dotenv import load_dotenv

load_dotenv()

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

with open("000095.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# event = {
#     "image_data": image_base64
# }
event = {
    "source": "s3",
    "bucket": "car-angle-classifier-images",
    "key": "000066.jpg"
}

result = requests.post(url, json=event).json()
print(result)
