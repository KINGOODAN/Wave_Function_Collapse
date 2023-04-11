import pygame
import random
import copy


class Tile:
    def __init__(self, stepx:int, stepy:int, size:int):
        self.stepx = stepx
        self.stepy = stepy
        self.size = size
        self.name = (f"images/test_image_{stepy*size}_{stepx*size}.png")
        self.image = pygame.image.load(self.name)
        self.sides:list[list[tuple[int,int,int,int]]] = []
        self.pixel = pygame.PixelArray(self.image)

        for i in range(4):
            self.sides.append([])
            for j in range(size):
                if i == 0:
                    self.sides[i].append(self.image.unmap_rgb(self.pixel[j][0])) #type: ignore
                if i == 1:
                    self.sides[i].append(self.image.unmap_rgb(self.pixel[self.size-1][j])) #type: ignore
                if i == 2:
                    self.sides[i].append(self.image.unmap_rgb(self.pixel[j][self.size-1])) #type: ignore
                if i == 3:
                    self.sides[i].append(self.image.unmap_rgb(self.pixel[0][j])) #type: ignore

        self.pixel.close()


class Slot:
    def __init__(self, pos: tuple[int,int], size:int, tile_size:int, base_tile_size:int, possibilities:list[Tile]): #scale is the multiplier the size is how many tile x then y
        self.pos: tuple[int,int] = pos
        self.size: int = size
        self.possibilities:list[Tile] = possibilities
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.tile: Tile
        self.collapsed = False
        self.entropy = self.size*self.size
        self.template = pygame.image.load("test_image.png")
        self.base_tile_size:int = base_tile_size
        self.tile_size:int = tile_size

    def draw(self):
        if self.collapsed:
            self.tile.image = pygame.transform.scale(self.tile.image, (self.tile_size, self.tile_size))
            self.screen.blit(self.tile.image, self.pos)
            
        
    def collapse(self):
        if len(self.possibilities) != 0:
            self.collapsed = True
            randomSlot = random.randint(0,len(self.possibilities)-1)
            self.tile = self.possibilities[randomSlot]


def determine_possibilities(grid:list[list[Slot]]):
    filter = []
    isDone = True
    for i,rows in enumerate(grid):
        for j,space in enumerate(rows):
            if space.collapsed == False:
                filter = copy.copy(space.possibilities)
                isDone = False
                if j+1 < len(grid[i]):
                    if grid[i][j+1].collapsed:
                        for possibility in space.possibilities:
                            if grid[i][j+1].tile.sides[3] != possibility.sides[1]:
                                #print(grid[i][j+1].tile.name, "LEFT DOES NOT MATCH", possibility.name, "RIGHT")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i][j+1].tile.name, "LEFT MATCHES", possibility.name, "RIGHT")
                if j-1 >= 0:
                    if grid[i][j-1].collapsed:
                        for possibility in space.possibilities:
                            if grid[i][j-1].tile.sides[1] != possibility.sides[3]:
                                #print(grid[i][j-1].tile.name, "RIGHT DOES NOT MATCH", possibility.name, "LEFT")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i][j-1].tile.name, "RIGHT MATCHES", possibility.name, "LEFT")
                if i+1 < len(grid):
                    if grid[i+1][j].collapsed:
                        for possibility in space.possibilities:
                            if grid[i+1][j].tile.sides[0] != possibility.sides[2]:
                                #print(grid[i+1][j].tile.name, "TOP DOES NOT MATCH", possibility.name, "BOTTOM")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i+1][j].tile.name, "TOP MATCHES", possibility.name, "BOTTOM")
                if i-1 >= 0:
                    if grid[i-1][j].collapsed:
                        for possibility in space.possibilities:
                            if grid[i-1][j].tile.sides[2] != possibility.sides[0]:
                                #print(grid[i-1][j].tile.name, "BOTTOM DOES NOT MATCH", possibility.name, "TOP")
                                filter.remove(possibility)
                            #else:
                                #print(grid[i-1][j].tile.name, "BOTTOM MATCHES", possibility.name, "TOP")
            space.possibilities = copy.copy(filter)
            space.entropy = len(space.possibilities)
    return isDone, grid


def collapse(size:int, grid:list[list[Slot]]):
    lowestEntropy = size*size
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


def makeGrid(screen:pygame.surface.Surface, grid:list[list[Slot]], img_tile_dimentions, tile_size:int, base_tile_size:int, possibilities:list[Tile]):
    grid = []
    for i in range(int(screen.get_height()/tile_size)):
        grid.append([])
        for j in range(int(screen.get_width()/tile_size)):
            grid[i].append(Slot((j*tile_size,i*tile_size), img_tile_dimentions, tile_size, base_tile_size, possibilities))
    return grid, False






        
        