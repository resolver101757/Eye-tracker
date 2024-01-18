import tkinter as tk
from PIL import Image, ImageTk
import cv2
from pathlib import Path
from fastai.vision.all import *
import json
import sys

# gets the right screen size for the current computer
if os.path.isfile('./current_device_home_laptop'):
    screen_location = "home_laptop"
elif os.path.isfile('./current_device_work_laptop'):
   screen_location = "work_screen"
else:
    print("no config found")
print("screen location : ", screen_location)

with open('screen_sizes.json', 'r') as f:
    screen_sizes = json.load(f)

# does this need to be in here.  
screen = screen_sizes[screen_location]
width = screen['width']
height = screen['height']
display_dims = (width, height)
print("screen dimensions : ", display_dims)

image_dims = (320,240)

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def get_y(fname):
    coords = fname.name.split('_')[1:]

    x, y = coords[0], coords[1].replace('.png', '') # assumes the files are formatted like so: "id_xcoord_ycoord.png"

    x = int(x)  / width
    y = int(y) / height
    coords = tensor([x,y])
    return coords

def imgname_to_coords(fname):
    # Extract coordinates from filename
    parts = fname.name.split('_')[1:]
    
    x, y = int(parts[-2]), int(parts[-1].replace('.png', ''))
    x_scaled, y_scaled = x / width, y / height

    # Return the scaled coordinates as a tensor
    return tensor([x_scaled, y_scaled]) #just need this for the fastai learner to load, this isn't used by the model


# Initialize the main window
root = tk.Tk()
root.title("Eye pos test")
root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_width = (screen_width // 2)
centre_height = (screen_height // 2)

# Set window dimensions
screen = {'width': width, 'height': height}  # Example dimensions
root.geometry(f"{screen['width']}x{screen['height']}")

# Create a canvas for drawing
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black')
canvas.pack()

def normalized_coords_to_coords(n_coords):
    xcoord = n_coords[0] * width
    ycoord = n_coords[1] * height
    return xcoord
