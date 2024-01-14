# Re-written get_data.py using tkinter instead of pygame

import cv2
import tkinter as tk
import random
from datetime import datetime
import os


# gets the right screen size for the current computer
if os.path.isfile('./current_device_home_laptop'):
    screen_locaton = "home_laptop"
else:
    print("File does not exist")

# Directory to save captured images
save_dir = "G:\My Drive\Learning\data_science\datasets\gaze-points"
save_dir = f"{save_dir}\{screen_locaton}"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Function to capture and save the image
def capture_and_save(x, y):
    ret, frame = camera.read()
    if ret:
        # Get current date and time for filename
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        filename = f'capture_{timestamp}_{x}_{y}.png'
        filename = os.path.join(save_dir, f'{timestamp}_{x}_{y}.png')
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")

# Main window setup
root = tk.Tk()
root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_width = (screen_width // 2)
centre_height = (screen_height // 2)

# Canvas for drawing
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black')
canvas.pack()

# Function to update the position of the "X"
def update_position():
    x, y = random.randint(0, screen_width), random.randint(0, screen_height)
    canvas.delete("all")
    canvas.create_text(x, y, text="X", font=("Arial", 74), fill="white")
    canvas.create_text(center_width, centre_height, text=f"co-ordinates w {x} and h {y}", font=("Arial", 20), fill="white")
    return x, y

# Initialize "X" position
x, y = update_position()

# Bind keys
def on_key_press(event):
    global x, y
    if event.char == 's':
        capture_and_save(x, y)
        x, y = update_position()
    elif event.char == 'c':
        x, y = update_position()
    elif event.char == 'q':
        root.destroy()
        camera.release()

root.bind('<Key>', on_key_press)

# Start the application
root.mainloop()
