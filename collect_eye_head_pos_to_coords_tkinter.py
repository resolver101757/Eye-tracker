# This Python script uses Tkinter and OpenCV to create a full-screen application that captures and saves images from a camera when a key is pressed,
# with the images being named based on the current timestamp and screen coordinates.

import cv2
import tkinter as tk
import random
from datetime import datetime
import os

# Initialize the camera
camera = cv2.VideoCapture(0)

# gets the right screen size for the current computer
if os.path.isfile('./current_device_home_laptop'):
    screen_locaton = "home-laptop"
    print(screen_locaton)
elif os.path.isfile('./current_device_work_laptop'):
    screen_locaton = "work-laptop"
    print(screen_locaton)
else :
    print("No current device file found")

# Directory to save captured images
save_dir = "G:\My Drive\Learning\data_science\datasets\gaze-points"
save_dir = f"{save_dir}\{screen_locaton}"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# Function to capture and save the image
def capture_and_save(x, y):
    ret, frame = camera.read()
    if ret:
        # Flip the frame horizontally
        if screen_locaton == "work-laptop":
            frame = cv2.flip(frame, 0)
        else: 
            frame = cv2.flip(frame, 1)
        # Get current date and time for filename
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        filename = f'capture_{timestamp}_{x}_{y}.png'
        
        filename = os.path.join(save_dir, f'{timestamp}-hieght{screen_width}-width{screen_height}-computer{screen_locaton}_{x}_{y}.png')
        print(f"Saving image as {filename}")
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    else:
        print("Error capturing image")

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
