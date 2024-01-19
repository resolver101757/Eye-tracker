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


temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


def get_y(fname):
    coords = fname.name.split('_')[1:]

    x, y = coords[0], coords[1].replace('.png', '') # assumes the files are formatted like so: "id_xcoord_ycoord.png"

    x = int(x)  / screen_width
    y = int(y) / screen_height
    coords = tensor([x,y])
    return coords

model = load_learner(Path(r"G:\My Drive\Learning\data_science\models\eye-tracker\20240112_140058_eye_tracker-first_save_after_correct_screen_size.pkl"), cpu=True)

def normalized_coords_to_coords(n_coords):
    xcoord = n_coords[0] * screen_width
    ycoord = n_coords[1] * screen_height
    return xcoord , ycoord

# Function to capture image and process it
def capture_image(event):
    # Capture the image
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # Optionally save or show the image here
        cv2.imwrite("captured_image.jpg", frame)  # Save the captured image

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.flip(frame, 0)

        # Here you would pass 'frame' to your model
        # For example: predicted_x, predicted_y = your_model.predict(frame)
        # For demonstration, using dummy coordinates (100, 100)
        
        
        pred = model.predict(img)
        new_pred = normalized_coords_to_coords(pred[0])

        predicted_x, predicted_y = new_pred
        print(f"predicted positions, predicted_x: {predicted_x}, predicted_y: {predicted_y}")

        # Draw the predicted 'X' on the canvas
        draw_x(predicted_x, predicted_y, 'red')
        
        # Generate random coordinates
        random_x, random_y = generate_random_coords()
        print(f"source postionn to predict (in loop), random_x: {random_x}, random_y: {random_y}")
        draw_x(random_x, random_y, 'green')

# Function to draw an 'X' on the canvas
def draw_x(x, y, color):
    size = 10
    canvas.create_line(x - size, y - size, x + size, y + size, fill=color)
    canvas.create_line(x + size, y - size, x - size, y + size, fill=color)

def generate_random_coords():
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    return x, y

def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

# Create the main window
root = tk.Tk()
root.title("X Locator")
root.bind('<Escape>', exit_fullscreen)

# Set the window to fullscreen
root.attributes('-fullscreen', True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(f"screen_width: {screen_width}, screen_height: {screen_height}")

# Create a canvas and place the initial 'X'
canvas = Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Generate random coordinates
random_x, random_y = generate_random_coords()
print(f"source postionn to predict, random_x: {random_x}, random_y: {random_y}")
draw_x(random_x, random_y, 'green')

# Bind the 'c' key to the image capture function
root.bind('<c>', capture_image)

# Run the application
root.mainloop()