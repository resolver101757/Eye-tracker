from fastai.basics import *
import pygame
from fastai.vision.all import *
import cv2
import pathlib


image_dims = (320,240)
display_dims = (3440,1440)


temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


def imgname_to_coords(fname):
    # Extract coordinates from filename
    parts = fname.name.split('_')[1:]
    
    x, y = int(parts[-2]), int(parts[-1].replace('.png', ''))
    x_scaled, y_scaled = x / 3440, y / 1440

    # Return the scaled coordinates as a tensor
    return tensor([y_scaled, x_scaled]) #just need this for the fastai learner to load, this isn't used by the model
 


def normalized_coords_to_coords(n_coords):
    xcoord = n_coords[1] * 3440
    ycoord = n_coords[0] * 1440
    return ycoord, xcoord

model = load_learner(Path('gaze_predictor.pkl'), False)

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