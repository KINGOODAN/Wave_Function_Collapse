import pygame
import random
import copy


class Tile:
    def __init__(self, filename:str, size:int):
        self.size = size
        self.name = filename
        self.image = pygame.image.load(f"images/{self.name}")
        self.sides:list[list[tuple[int,int,int,int]]] = []
        self.pixel = pygame.PixelArray(self.image)
        self.pixel_list:list[list[tuple[int,int,int,int]]] = []
        for i, pix in enumerate(self.pixel): #type: ignore
            self.pixel_list.append([])
            for j in pix:
                self.pixel_list[i].append(self.image.unmap_rgb(j))

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
    def __init__(self, pos: tuple[int,int], size:tuple[int,int], tile_size:int, base_tile_size:int, possibilities:list[Tile], image:str): #scale is the multiplier the size is how many tile x then y
        self.pos: tuple[int,int] = pos
        self.size: tuple[int,int] = size
        self.possibilities:list[Tile] = possibilities
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.tile: Tile
        self.collapsed = False
        self.entropy = self.size[0]*self.size[1]
        self.template = pygame.image.load(f"images/{image}")
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
                if j+1 < len(grid[i]) and grid[i][j+1].collapsed:
                    for possibility in space.possibilities:
                        if not check_sides(grid[i][j+1].tile.sides[3],possibility.sides[1]):
                            filter.remove(possibility)
                if j-1 >= 0 and grid[i][j-1].collapsed:
                    for possibility in space.possibilities:
                        if not check_sides(grid[i][j-1].tile.sides[1], possibility.sides[3]):
                            filter.remove(possibility)
                if i+1 < len(grid) and grid[i+1][j].collapsed:
                    for possibility in space.possibilities:
                        if not check_sides(grid[i+1][j].tile.sides[0], possibility.sides[2]):
                            filter.remove(possibility)
                if i-1 >= 0 and grid[i-1][j].collapsed:
                    for possibility in space.possibilities:
                        if not check_sides(grid[i-1][j].tile.sides[2], possibility.sides[0]):
                            filter.remove(possibility)
            space.possibilities = copy.copy(filter)
            space.entropy = len(space.possibilities)
    return isDone, grid


def collapse(grid:list[list[Slot]], num_pos:int):
    lowestEntropy = num_pos
    lowestList:list[Slot] = []
    for rows in grid:
        for s in rows:
            if not s.collapsed and s.entropy < lowestEntropy:
                lowestEntropy = s.entropy

    for rows in grid:
        for s in rows:
            if not s.collapsed and s.entropy == lowestEntropy:
                lowestList.append(s)

    if len(lowestList) != 0:
        randomSlot = random.randint(0,len(lowestList)-1)
        lowestList[randomSlot].collapse()
    return grid


def makeGrid(screen:pygame.surface.Surface, grid:list[list[Slot]], img_tile_dimentions:tuple[int,int], tile_size:int, base_tile_size:int, possibilities:list[Tile],image:str):
    grid = []
    for i in range(int(screen.get_height()/tile_size)):
        grid.append([])
        for j in range(int(screen.get_width()/tile_size)):
            grid[i].append(Slot((j*tile_size,i*tile_size), img_tile_dimentions, tile_size, base_tile_size, possibilities, image))
    return grid, False


def check_sides(side1:list[tuple[int,int,int,int]], side2:list[tuple[int,int,int,int]]):
    dif_val = 0
    if side1 == side2:
        return True
    else:
        for i in range(len(side1)):
            if side1[i] != side2[i]:
                dif_val += 1
    check = len(side1)*0.15
    if dif_val < check:
        return True
    return False







        
        