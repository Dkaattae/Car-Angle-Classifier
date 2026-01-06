# Car-Angle-Classifier
This project builds an image classification system that determines the viewing angle of a vehicle from a single image. Given an input image, the model classifies it into one of four categories: front view, rear view, side view, or not a car.

note: not a car meaning not a full car exterior view, it could be a part of the car, interior, multiple cars.

# data downloading
using duckduckgo search engine to download images with the search query as tag.   
then go through each image to check correctness.    
note: there are room for improvement for search queries. e.g. my car {angle} view parking lot shows parking lot instead of a car.   
all files are loaded into google drive, so it is easier to load into google colab for training.   

# data split
using sklearn train test split to split data from the metadata csv file.  

# training

# validation

# metrics

# deploy