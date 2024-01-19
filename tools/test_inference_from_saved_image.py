# This Python script uses a pre-trained model to predict the x and y coordinates of a gaze from images in a specified directory.
# It then compares these predicted coordinates with the actual coordinates, which are extracted from the image filenames.
# The script prints out the differences between the predicted and actual coordinates for each image.

from fastai.basics import *
from fastai.vision.all import *
import cv2
import pathlib
import json
import os
import tkinter as tk
from PIL import Image, ImageTk
import sys
from PIL import Image
import os

# directory of images to predict against 
directory = r"C:\development\github projects\Eye-tracker\captured_images"


width = 2560
height = 1440

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def get_y(fname):
    """
    Extracts the x and y-coordinate from the given filename.

    Parameters:
    fname (str): The filename containing the coordinates.

    Returns:
    torch.Tensor: The y-coordinate extracted from the filename.
    """
    coords = fname.name.split('_')[1:]

    x, y = coords[0], coords[1].replace('.png', '') # assumes the files are formatted like so: "id_xcoord_ycoord.png"

    x = int(x)  / width
    y = int(y) / height
    coords = tensor([x,y])
    return coords


#model_path = str(Path(r"G:\My Drive\Learning\data_science\models\eye-tracker\dans_gaze_predictor.pkl"))

model_path = str(Path(r"G:\My Drive\Learning\data_science\models\eye-tracker\20240111_171100_eye_tracker.pkl"))


model = load_learner(model_path, cpu=True)

image_dims = (320,240)


def normalized_coords_to_coords(n_coords):
    xcoord = n_coords[0] * width
    ycoord = n_coords[1] * height
    return xcoord, ycoord



def predict_coords(img):
    # prediction 
    pred = model.predict(img)
    pred_normalised = normalized_coords_to_coords(pred[0])
    print(pred)
    print(pred_normalised)
    return(pred_normalised)

def imgname_to_coords(fname):
    # Extract coordinates from filename
    parts = fname.name.split('_')[1:]
    x, y = int(parts[-2]), int(parts[-1].replace('.png', ''))
    print(f"X coords are {x} and y coords are {y}")
    
    return(x,y) 


def compare_prediction_with_actual(image_path, image_dims):
    # get image and format 
    img = Image.open(image_path)
    img = img.resize(image_dims)
    pred_normalised = predict_coords(img)
    file_name_coords = imgname_to_coords(Path(image_path))
    print("X difference between predicted and actual " , abs(pred_normalised[0] - file_name_coords[0]), "Y difference between predicted and actual ", abs(pred_normalised[1] - file_name_coords[1]))
    print(abs(pred_normalised[0] - file_name_coords[0]) / width, abs(pred_normalised[1] - file_name_coords[1]) / height)
    

for filename in os.listdir(directory):
    if filename.endswith(".png"):
        image_path = os.path.join(directory, filename)
        compare_prediction_with_actual(image_path, image_dims)


