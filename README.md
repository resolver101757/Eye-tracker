# Eye-Tracking Project

## Introduction

Why have mouse when you can have eye tracking? Modern computers have cameras, screens, and faster and more efficient GPUs to run neural networks.  This project aims to train a model for eye-tracking to co-ordinates. The model is trained on a dataset of images captured in different lighting conditions, distances, postures, head rotations, and offsets.

## Project Structure

### Directories

- `tools/`: Directory containing various utility scripts and notebooks.
- `training/`: Directory containing Jupyter notebooks for training the model.

### root files 

- `test_eye_position_using_model_tkinter.py`: Script for testing eye position using the trained model and Tkinter.
- `collect_eye_head_pos_to_coords_tkinter.py`: Script for collecting eye and head position data using Tkinter.
- `screen_sizes.json`: JSON file containing screen size data.

## Setup

Install python and the following packages:

pip install opencv-python
pip install python-tk
pip install numpy
pip install fastai
pip install Pillow

## Usage

To start data collection (image to coordinates) run the following script and make sure you've selected the right camera - cv2.VideoCapture(1):

- collect_eye_head_pos_to_coords_tkinter.py

For testing the model there's a few scripts depending on how you want to test :

To test the model run the following script and make sure you've selected the right camera, just change the line to the appropriate number cv2.VideoCapture(1):

- tools/test_inference_taking_a_pic.py

This will run though the saved images and show the actual to predicted coordinates.

- tools/test_inference_from_saved_image.py

Here's a few other scripts that might be useful for understanding the hardware, e.g. camera, screen size, etc:

- tools/get_screen_sizes.py
- tools/get_screen_sizes_pygame.py
- tools/test_camera_with_openCV.py

## Future Work

- The model's accuracy could potentially be improved by feeding in additional features such as distance to face, rotation of head, rotation of eyes, head offset, camera offset and rotation, and screen dimensions. Tools like facial landmarking models could be used to track head rotation and offset, and possibly distance with some maths around distance between features accounting for rotation.

- using a depth camera could also be used to get distance to face and head rotation mitigating the need for facial landmarking models.

- intergrating the model into windows to control the mouse.

- All modern laptops have a camera and most are windows hello certified, they also have a infrared camera too. This could be used to see in low light conditions and would help see pupils better in the dark or light conditions.  However, i havent been able to find a way to access the infrared camera in python.  Any suggestions would be appreciated.

- Try differnt models and see if they improve accuracy
 - transfomer model but might neeed to be much bigger to get good results.
 - cnn model with more layers.

Contributing

Contributors are welcome! Please fork the repository, make your changes, and submit a pull request. Adhere to our coding standards (Python, non-PEP8), include tests for new features, and update documentation as necessary. For any questions or discussions, use our GitHub issues section.
