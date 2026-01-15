FROM public.ecr.aws/lambda/python:3.12
WORKDIR /var/task

RUN pip install onnxruntime pillow numpy boto3

COPY car_angle_classifier.onnx car_angle_classifier.onnx.data ./
COPY labels_fixed.csv ./
COPY lambda_function.py ./

CMD ["lambda_function.lambda_handler"]