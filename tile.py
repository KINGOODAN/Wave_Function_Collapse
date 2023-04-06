import pygame
import random
import copy
import numpy as np



class Tile:
    def __init__(self, image:pygame.surface.Surface, stepx:int, stepy:int, size:tuple[int,int]):
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
            self.sides.append(image.unmap_rgb(self.pixel[self.check_positions[i]])) #type: ignore
            #print(image.unmap_rgb(self.pixel[self.check_positions[i]]),end=", ") #type: ignore
            #print(self.check_positions[i])

class Slot:
    def __init__(self, pos: tuple[int,int], scale: int, size: tuple[int,int]): #scale is the multiplier the size is how many tile x then y
        self.pos: tuple[int,int] = pos
        self.scale: int = scale
        self.size: tuple[int,int] = size
        self.possibilities:list[Tile] = []
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.tile: Tile
        self.collapsed = False
        self.entropy = self.size[0]*self.size[1]
        self.template = pygame.image.load("test_image.png")
        self.pixel = None

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.possibilities.append(Tile(self.template,i,j,(100,100))) 

    def draw(self):
        if self.collapsed:
            self.tile.image = pygame.transform.scale(self.template, (216, 216))
            self.screen.blit(self.tile.image, self.pos,(54*self.tile.stepx,54*self.tile.stepy,54,54),)
            
        
    def collapse(self):
        #print("test")
        if len(self.possibilities) != 0:
            print("______test")
            self.collapsed = True
            randomSlot = random.randint(0,len(self.possibilities)-1)
            self.tile = self.possibilities[randomSlot]
            
        


def determine_possibilities(grid:list[list[Slot]]):
    filter = []
    isDone = True
    for i,rows in enumerate(grid):
        for j,t in enumerate(rows):
            if t.collapsed == False:
                filter = copy.copy(t.possibilities)
                isDone = False
                if j+1 < len(grid[i]):
                    if grid[i][j+1].collapsed:
                        for possibility in t.possibilities:
                            if grid[i][j+1].tile.sides[3] != possibility.sides[1]:
                                filter.remove(possibility)
                if j-1 >= 0:
                    if grid[i][j-1].collapsed:
                        for possibility in t.possibilities:
                            if grid[i][j-1].tile.sides[1] != possibility.sides[3]:
                                filter.remove(possibility)
                if i+1 < len(grid):
                    if grid[i+1][j].collapsed:
                        for possibility in t.possibilities:
                            if grid[i+1][j].tile.sides[0] != possibility.sides[2]:
                                filter.remove(possibility)
                if i-1 >= 0:
                    if grid[i-1][j].collapsed:
                        for possibility in t.possibilities:
                            if grid[i-1][j].tile.sides[2] != possibility.sides[0]:
                                filter.remove(possibility)
            t.possibilities = copy.copy(filter)
            t.entropy = len(t.possibilities)
    return isDone, grid

def collapse(size:tuple[int,int], grid:list[list[Slot]]):
    lowestEntropy = size[0]*size[1]
    lowestList:list[Slot] = []
    for rows in grid:
        for s in rows:
            if s.collapsed == False:
                if s.entropy < lowestEntropy:
                    lowestEntropy = s.entropy
    for rows in grid:
        for s in rows:
            if s.collapsed == False:
                if s.entropy == lowestEntropy:
                    lowestList.append(s)

    if len(lowestList) != 0:
        randomSlot = random.randint(0,len(lowestList)-1)
        lowestList[randomSlot].collapse()
    return grid



def makeGrid(screen:pygame.surface.Surface, grid:list[list[Slot]]):
    grid = []
    scale = 54
    for i in range(int(screen.get_height()/scale)):
        grid.append([])
        for j in range(int(screen.get_width()/scale)):
            grid[i].append(Slot((j*scale,i*scale), scale, (4,4)))
    return grid






        
        