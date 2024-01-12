from fastai.basics import *
import pygame
from fastai.vision.all import *
import cv2
import pathlib
import json

with open('screen_sizes.json', 'r') as f:
    screen_sizes = json.load(f)

screen = screen_sizes['work_screen']
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
 


def normalized_coords_to_coords(n_coords):
    xcoord = n_coords[1] * width
    ycoord = n_coords[0] * height
    return ycoord, xcoord

model = load_learner(Path(r'G:\My Drive\Learning\data_science\models\eye-tracker\20240112_133240_eye_tracker-first_save_after_correct_screen_size.pkl'), cpu=True)

canvas = pygame.display.set_mode(display_dims)

cap = cv2.VideoCapture(0)

pygame.display.flip()
pygame.display.set_caption("Eye pos test")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    
    ret,frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    canvas.fill((0,0,0))

    img = Image.fromarray(frame).resize(image_dims)
    #img.show()
    pred = model.predict(img)
    
    new_pred = normalized_coords_to_coords(pred[0])
    print(pred[0], new_pred)
    pygame.draw.ellipse(canvas, 'red', pygame.Rect(new_pred[1], new_pred[0], 10, 10))
    pygame.display.update()

    #cv2.imshow('Gaze prediction', frame)
