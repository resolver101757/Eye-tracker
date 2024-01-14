from fastai.basics import *
from fastai.vision.all import *
import cv2
import pathlib
import json
import os
import tkinter as tk
from PIL import Image, ImageTk
import sys

# gets the right screen size for the current computer
if os.path.isfile('./current_device_home_laptop'):
    screen_locaton = "home_laptop"
else:
    print("no laptop found")

with open('screen_sizes.json', 'r') as f:
    screen_sizes = json.load(f)

# does this need to be in here.  
screen = screen_sizes[screen_locaton]
width = screen['width']
height = screen['height']
display_dims = (width, height)
print("screen dimensions : ", display_dims)

image_dims = (320,240)

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

def imgname_to_coords(fname):
    # Extract coordinates from filename
    parts = fname.name.split('_')[1:]
    
    x, y = int(parts[-2]), int(parts[-1].replace('.png', ''))
    x_scaled, y_scaled = x / width, y / height

    # Return the scaled coordinates as a tensor
    return tensor([y_scaled, x_scaled]) #just need this for the fastai learner to load, this isn't used by the model


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
    xcoord = n_coords[1] * width
    ycoord = n_coords[0] * height
    return ycoord, xcoord

# load the model
model = load_learner(Path(r'G:\My Drive\Learning\data_science\models\eye-tracker\20240112_140058_eye_tracker-first_save_after_correct_screen_size.pkl'), cpu=True)

cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame).resize(image_dims)
        pred = model.predict(img)

        new_pred = normalized_coords_to_coords(pred[0])
        canvas.delete("all")
        canvas.create_oval(new_pred[1]-5, new_pred[0]-5, new_pred[1]+5, new_pred[0]+5, fill='red')

    root.after(10, update_frame)

def on_closing():
    cap.release()
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
update_frame()
root.mainloop()