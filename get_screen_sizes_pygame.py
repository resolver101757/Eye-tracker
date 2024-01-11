import pygame

# Initialize Pygame
pygame.init()

# Get screen resolution
infoObject = pygame.display.Info()

# Print screen width and height
print("Screen width: ", infoObject.current_w)
print("Screen height: ", infoObject.current_h)