import requests
import base64


url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

with open("000095.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

##### image #####
# event = {
#     "image_data": image_base64
# }

##### url #####
event = {
    "url": "https://media.wired.com/photos/5e7b7a0fadfa9d0008e095b2/master/w_2560%2Cc_limit/Transpo-selfdrivingcar-1158000221.jpg"
}

# event = {
#     "source": "s3",
#     "bucket": "car-angle-classifier-images",
#     "key": "000066.jpg"
# }

result = requests.post(url, json=event).json()
print(result)
