# get the coordinates of the X and save the image
import pygame
import cv2
import random
import os
from datetime import datetime

# Initialize Pygame and the camera
pygame.init()
camera = cv2.VideoCapture(1)  # Adjust the camera index if needed

# Get screen size and create a fullscreen window
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen_width, screen_height = infoObject.current_w, infoObject.current_h

print ("screen_width = ", screen_width)
print ("screen_height = ", screen_height)

import random

def get_random_coordinate(screen_width, screen_height, edge_size, mode = 'whole'):
    if mode == 'edge':
        # Define edge regions
        top_edge = (random.randint(0, screen_width), random.randint(0, edge_size))
        bottom_edge = (random.randint(0, screen_width), random.randint(screen_height - edge_size, screen_height))
        left_edge = (random.randint(0, edge_size), random.randint(0, screen_height))
        right_edge = (random.randint(screen_width - edge_size, screen_width), random.randint(0, screen_height))
        # Randomly choose an edge region
        return random.choice([top_edge, bottom_edge, left_edge, right_edge])
    elif mode == 'whole':
        # Return a random coordinate within the whole screen
        return (random.randint(0, screen_width), random.randint(0, screen_height))
    elif mode == 'centre':
        # Return a random coordinate near the centre of the screen
        centre_x = screen_width // 2
        centre_y = screen_height // 2
        return (random.randint(centre_x - edge_size, centre_x + edge_size), random.randint(centre_y - edge_size, centre_y + edge_size))
    else:
        raise ValueError("Invalid mode. Choose from 'edge', 'whole', or 'centre'.")


# Directory to save captured images
save_dir = "G:\My Drive\Learning\data_science\datasets\gaze-points"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Function to capture and save the image
def capture_and_save(x, y):
    ret, frame = camera.read()
    if ret:
        # Vertically flip the image
        flipped_frame = cv2.flip(frame, 0)

        # Get current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")

        filename = os.path.join(save_dir, f'{timestamp}_{x}_{y}.png')
        cv2.imwrite(filename, flipped_frame)
        print(f"Image saved as {filename}")

    # Generate new coordinates for "X"
    return get_random_coordinate(screen_width, screen_height, 100)  # Adjust edge_size as needed

# Initial position of the "X"
x, y = get_random_coordinate(screen_width, screen_height, 100)  # Adjust edge_size as needed



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                x, y = capture_and_save(x, y)
            elif event.key == pygame.K_c:  # Skip without saving
                x, y = get_random_coordinate(screen_width, screen_height, 100)  # Adjust edge_size as needed
            elif event.key is pygame.K_q:
                running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Display the "X" at the current position
    font = pygame.font.Font(None, 74)
    text = font.render("X", True, (255, 255, 255))
    screen.blit(text, (x, y))

    # Update the display
    pygame.display.flip()

# Release resources
camera.release()
pygame.quit()
