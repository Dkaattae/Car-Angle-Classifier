# deploy in cloud

## test event from s3
test locally with dotenv
i have my aws credentials export to local environment. 
```
docker run -it --rm \
    -p 8080:8080 \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    car-angle-classifier
```

## push to AWS ECR
```
aws ecr create-repository \
    --repository-name car-angle-classifier-zoomcamp \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-2
```

`aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 344988460968.dkr.ecr.us-east-2.amazonaws.com/car-angle-classifier-zoomcamp`

## deploy to AWS ECR
```
docker tag car-angle-classifier:latest 344988460968.dkr.ecr.us-east-2.amazonaws.com/car-angle-classifier-zoomcamp:latest
docker push 344988460968.dkr.ecr.us-east-2.amazonaws.com/car-angle-classifier-zoomcamp:latest
```
