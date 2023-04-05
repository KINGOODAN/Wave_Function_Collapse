import pygame
import random

class Tile:
    def __init__(self, image:pygame.image):
        self.image = image
        self.pixel = pygame.PixelArray(self.image)
        self.sides = []
        self.check_positions = [
            (int(self.image.get_width()/2),0),
            (self.image.get_width()/2,int(self.image.get_height())),
            (0,int(self.image.get_height()/2)),
            (self.image.get_width(),int(self.image.get_height()/2)),
        ]
        for i in range(4):
            self.sides.append(image.pygame.Surface.unmap_rgb(self.pixel[self.check_positions[i]]))