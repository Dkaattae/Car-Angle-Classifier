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
