# This program is a Python-based eye-tracking application that uses a webcam to capture images, processes them with a deep learning model to predict gaze coordinates, 
# and displays these predictions on a full-screen graphical interface. It integrates technologies like OpenCV for image capture, FastAI for model prediction, and Tkinter 
# for the user interface, offering an interactive and visual demonstration of eye-tracking technology.

import tkinter as tk
from tkinter import Canvas
import cv2
from PIL import Image, ImageTk
import numpy as np
from fastai.basics import *
from fastai.vision.all import *
import pathlib
import sys
import random

# this is a hack to get the model to load on windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# opens the webcam
cap = cv2.VideoCapture(1)

# sets the initial capture counter to 0
# used for labeling predicted and actual coordinates printed on the screen 
capture_counter = 0

# not used for inference 
# but needed for the model Pickle to load
def get_y(fname):
    coords = fname.name.split('_')[1:]

    x, y = coords[0], coords[1].replace('.png', '') # assumes the files are formatted like so: "id_xcoord_ycoord.png"

    x = int(x)  / screen_width
    y = int(y) / screen_height
    coords = tensor([x,y])
    return coords

# lodas model from pickle 
model = load_learner(Path(r"G:\My Drive\Learning\data_science\models\eye-tracker\20240112_140058_eye_tracker-first_save_after_correct_screen_size.pkl"), cpu=True)

# Convert normalized coordinates to screen coordinates
def normalized_coords_to_coords(n_coords):
    xcoord = n_coords[0] * screen_width
    ycoord = n_coords[1] * screen_height
    return xcoord , ycoord


# capture image and process model 
def capture_image(event):
    global capture_counter  # Declare capture_counter as global
    # Capture the image
    ret, frame = cap.read()
      
    if ret:        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.flip(frame, 0)
        pred = model.predict(img)
        new_pred = normalized_coords_to_coords(pred[0])

        predicted_x, predicted_y = new_pred
        print(f"predicted positions, predicted_x: {predicted_x}, predicted_y: {predicted_y}")

        # Draw the predicted 'X' on the canvas
        draw_x(predicted_x, predicted_y, 'red', capture_counter)
        capture_counter += 1

        
        # Generate random coordinates
        random_x, random_y = generate_random_coords()
        print(f"source postionn to predict (in loop), random_x: {random_x}, random_y: {random_y}")
        draw_x(random_x, random_y, 'green', capture_counter)
        

# draws an 'X' on the canvas
def draw_x(x, y, color, number):
    size = 10
    canvas.create_line(x - size, y - size, x + size, y + size, fill=color)
    canvas.create_line(x + size, y - size, x - size, y + size, fill=color)
    canvas.create_text(x + size + 5, y, text=str(number), fill=color)

# generates random coordinates so that the user can look at the 'X' and the model can predict the coordinates from the picture taken 
def generate_random_coords():
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    return x, y

# exits full screen mode
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

# Create the main window
root = tk.Tk()
root.title("X Locator")
root.bind('<Escape>', exit_fullscreen)

# Set the window to fullscreen and get the screen dimensions
root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(f"screen_width: {screen_width}, screen_height: {screen_height}")

# Create a canvas for placing the 'X' and the predicted 'X'
canvas = Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Generate random coordinates
random_x, random_y = generate_random_coords()
print(f"source postionn to predict, random_x: {random_x}, random_y: {random_y}")
draw_x(random_x, random_y, 'green', capture_counter)
capture_counter += 1

# Bind the 'c' key to the image capture function
root.bind('<c>', capture_image)

# Run the application
root.mainloop()
cap.release()