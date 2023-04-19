import pygame
from pygame.locals import * #type: ignore
from tile import *
from PIL import Image
from itertools import product
import os
import shutil

list_of_input_images = ["test_image.png","wires_test.png","maze1.png"]

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.grid:list[list[Slot]] = []
        self.done:bool = False
        self.image = list_of_input_images[2]
        self.image_dir = "images/"
        self.img = Image.open(self.image_dir + self.image)
        self.image_size:tuple[int,int] = self.img.size
        self.base_tile_size = 100
        self.possable_tile_sizes = {"A":120,"B":60,"C":40,"D":30,"E":24,"F":20}
        self.tile_size:int = 120
        self.img_tile_dimentions:tuple[int,int] = (int(self.image_size[0]/self.base_tile_size),int(self.image_size[1]/self.base_tile_size))
        self.possibilities:list[Tile] = [] 

    def run(self):
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    self.tile_size = self.possable_tile_sizes["A"]
                    break
                elif event.key == K_2:
                    self.tile_size = self.possable_tile_sizes["B"]
                    break
                elif event.key == K_3:
                    self.tile_size = self.possable_tile_sizes["C"]
                    break
                elif event.key == K_4:
                    self.tile_size = self.possable_tile_sizes["D"]
                    break
                elif event.key == K_5:
                    self.tile_size = self.possable_tile_sizes["E"]
                    break
                elif event.key == K_6:
                    self.tile_size = self.possable_tile_sizes["F"]
                    break
        self.slice(self.image, self.image_dir, self.image_dir, self.base_tile_size)
        self.make_possibilities()
        self.grid, self.done = makeGrid(self.screen, self.grid, self.img_tile_dimentions, self.tile_size, self.base_tile_size, self.possibilities, self.image)
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            if keys[pygame.K_LSHIFT]:
                self.grid, self.done = makeGrid(self.screen, self.grid, self.img_tile_dimentions, self.tile_size, self.base_tile_size, self.possibilities, self.image)

            self.screen.fill((0,0,0))

            if not self.done: #type: ignore
                self.done,self.grid = determine_possibilities(self.grid)
                self.grid = collapse(self.grid, len(self.possibilities))

            for i in range(int(self.screen.get_height()/self.tile_size)):
                for j in range(int(self.screen.get_width()/self.tile_size)):
                    self.grid[i][j].draw()

            pygame.display.flip()
        self.clear_folder()

    def slice(self, filename, dir_in, dir_out, d):
        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(dir_in, filename))
        w, h = img.size
        
        grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
        for i, j in grid:
            box = (j, i, j+d, i+d)
            for k in range(4):
                out = os.path.join(dir_out, f'{name}_{i}_{j}_{90*k}{ext}')
                img.crop(box).rotate(90*k).save(out)

    
    def clear_folder(self, check_list = []):
        folder = self.image_dir
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if filename not in check_list:
                try:
                    if filename in list_of_input_images:
                        pass
                    elif os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        

    def make_possibilities(self):
        temp:list[Tile] = []
        for filename in os.listdir(self.image_dir):
            if filename not in list_of_input_images:
                self.possibilities.append(Tile(filename,self.base_tile_size))

        for tile in self.possibilities:
            present = False
            for otherTile in temp:
                if tile.pixel_list == otherTile.pixel_list:
                    present = True

            if not present:
                temp.append(tile) 

        self.possibilities = copy.copy(temp)
        temp2 = []
        for i in self.possibilities:
            temp2.append(i.name)
        self.clear_folder(temp2)