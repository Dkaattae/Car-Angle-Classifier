# Car-Angle-Classifier
This project builds an image classification system that determines the viewing angle of a vehicle from a single image. Given an input image, the model classifies it into one of four categories: front view, rear view, side view.   

## data downloading
using duckduckgo search engine to download images with the search query as tag.   
then go through each image to check correctness.    
note: there are room for improvement for search queries. e.g. my car {angle} view parking lot shows parking lot instead of a car.   
all files are loaded into google drive, so it is easier to load into google colab for training.   

## data split
using sklearn train test split to split data from the metadata csv file.  
after getting rid of bad images, and randomly split all images.   
count in training set.    
front: 272, rear: 203, side: 238.  

## training
first attempt: original
first best val acc: 
second attempt: more augmentation, 10 epochs
second best val acc: 0.8239
third attempt: less augmentation (continue training), 10 epochs
third best val acc: 0.8380
fourth attempt: dropout and inner layer, 50 epochs
fourth best val acc: 0.8590

best model is saved and exported to onnx

## deploy
run locally
```
docker build -t car-angle-classifier .
docker run -it --rm \
    -p 8080:8080 \
    car-angle-classifier
```
open another terminal, python test.py.  

run in cloud.  
test locally
i have my aws credentials export to local environment. 
```
docker run -it --rm \
    -p 8080:8080 \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    car-angle-classifier
```

```
aws ecr create-repository \
    --repository-name car-angle-classifier-zoomcamp \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-2
```

`aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 344988460968.dkr.ecr.us-east-2.amazonaws.com/car-angle-classifier-zoomcamp`

```
docker tag car-angle-classifier:latest 344988460968.dkr.ecr.us-east-2.amazonaws.com/car-angle-classifier-zoomcamp:latest
docker push 344988460968.dkr.ecr.us-east-2.amazonaws.com/car-angle-classifier-zoomcamp:latest
```

### API Gateway
https://w5za34is7b.execute-api.us-east-2.amazonaws.com


```
curl -X POST \
  https://w5za34is7b.execute-api.us-east-2.amazonaws.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "source": "s3",
    "bucket": "car-angle-classifier-images",
    "key": "000290.jpg"
  }'
  ```

### bash command
`chmod +x deploy.sh`
`./deploy.sh`