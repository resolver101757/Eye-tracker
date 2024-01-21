# gets teh screen size using pyqt5 and pygame and prints it out

import pygame
import cv2
import random
import os
from datetime import datetime
import random

# Initialize Pygame and the camera
pygame.init()
infoObject = pygame.display.Info()
print(infoObject)

from PyQt5.QtWidgets import QApplication

app = QApplication([])
screen_rect = app.primaryScreen().availableGeometry()
screen_width, screen_height = screen_rect.width(), screen_rect.height()

print("Screen width:", screen_width)
print("Screen height:", screen_height)
