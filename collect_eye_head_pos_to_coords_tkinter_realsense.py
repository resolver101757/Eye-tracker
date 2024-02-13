## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
import random
from datetime import datetime
import os

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
save_dir = f"{save_dir}\{screen_locaton}\depth_and_color_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# Function to capture and save the image
def capture_and_save(x, y):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    # Get current date and time for filename
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    filename = f'capture_{timestamp}_{x}_{y}.png'
    
    filename = os.path.join(save_dir, f'{timestamp}-hieght{screen_width}-width{screen_height}-computer{screen_locaton}_{x}_{y}.png')
    print(f"Saving image as {filename}")
    

    # Show images
    # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('RealSense', images)
    # cv2.waitKey(1)
    
    # Save color and depth images
    color_img_path = os.path.join(save_dir, f'{timestamp}-hieght{screen_width}-width{screen_height}-computer{screen_locaton}-depth_{x}_{y}.png')
    depth_img_path = os.path.join(save_dir, f'{timestamp}-hieght{screen_width}-width{screen_height}-computer{screen_locaton}-colour_{x}_{y}.png')


    cv2.imwrite(color_img_path, color_image)
    cv2.imwrite(depth_img_path, depth_colormap)
    print(f"Color image saved at {color_img_path}")
    print(f"Depth image saved at {depth_img_path}")


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
count = 0
warmup_frames = 20 

# warm up the camera so it can adjust to the lighting
for i in range(0, warmup_frames):
    count += 1
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
            # Warm-up phase to allow camera to adjust
    print(f"Warming up... {count}/{warmup_frames}")
        

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
        # Stop streaming
        pipeline.stop()

root.bind('<Key>', on_key_press)

# Start the application
root.mainloop()


