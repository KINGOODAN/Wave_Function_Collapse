import pygame
import random

class Tile:
    def __init__(self, image:pygame.image, stepx:int, stepy:int, size:tuple[int,int]):
        self.image = image
        self.stepx = stepx
        self.stepy = stepy
        self.size = size
        self.pixel = pygame.PixelArray(self.image)
        self.sides = []
        self.check_positions = [
            (size[0]//2 + stepx * size[0],stepy * size[1]),
            (size[0]//2 + stepx * size[0],((stepy + 1) * size[1])-1),
            (stepx * size[0],size[1]//2 + stepy * size[1]),
            (((stepx + 1) * size[0])-1, size[1]//2 + stepy * size[1]),
        ]
        for i in range(4):
            self.sides.append(image.unmap_rgb(self.pixel[self.check_positions[i]]))
            print(image.unmap_rgb(self.pixel[self.check_positions[i]]),end=", ")
            print(self.check_positions[i])
        
        