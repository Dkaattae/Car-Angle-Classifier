#!/bin/bash

IMAGE_NAME="car-angle-classifier"
AWS_REGION="us-east-2"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r ".Account")

COMMIT_SHA=$(git rev-parse --short HEAD)
DATETIME=$(date +"%Y%m%d-%H%M%S")
IMAGE_TAG="${COMMIT_SHA}-${DATETIME}"

ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_URI="${ECR_URI}/${IMAGE_NAME}-zoomcamp:${IMAGE_TAG}"

aws ecr get-login-password \
  --region ${AWS_REGION} \
| docker login \
  --username AWS \
  --password-stdin ${ECR_URI}

docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_URI}
docker push ${IMAGE_URI}

aws lambda update-function-code \
  --function-name car-angle-classifier-lambda \
  --image-uri ${IMAGE_URI} \
  --region ${AWS_REGION}