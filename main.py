import pygame
from tile import *
from PIL import Image
from itertools import product
import os
import shutil

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.grid:list[list[Slot]] = []
        self.done:bool = False
        self.tile_size:int = 120
        self.img_tile_dimentions:int = 4
        self.image = "test_image.png"

    def run(self):
        self.tiles(self.image, ".", "images/", 100)
        self.grid = makeGrid(self.screen, self.grid, self.tile_size, self.img_tile_dimentions)
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            if keys[pygame.K_LSHIFT]:
                self.grid = makeGrid(self.screen, self.grid, self.tile_size, self.img_tile_dimentions)

            self.screen.fill((0,0,0))

            if not self.done: #type: ignore
                self.done,self.grid = determine_possibilities(self.grid)
                self.grid = collapse(self.img_tile_dimentions, self.grid)

            for i in range(int(self.screen.get_height()/self.tile_size)):
                for j in range(int(self.screen.get_width()/self.tile_size)):
                    self.grid[i][j].draw()

            time = self.clock.tick() / 1000
            pygame.display.flip()
        self.clear_folder()

    def tiles(self, filename, dir_in, dir_out, d):
        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(dir_in, filename))
        w, h = img.size
        
        grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
        for i, j in grid:
            box = (j, i, j+d, i+d)
            out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
            img.crop(box).save(out)
    
    def clear_folder(self):
        folder = "images/"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))