import pygame
from tile import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.template = pygame.image.load("test_image.png")
        self.tile = Tile(self.template,3,3,(100,100))
        self.grid:list[list[Slot]]
        self.done:bool

    def run(self):
        
        makeGrid(self.screen, self.grid, self.done)

        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            if keys[pygame.K_LSHIFT]:
                makeGrid(self.screen, self.grid, self.done)

            self.screen.fill((0,0,0))

            if not done: #type: ignore
                done = determine_possibilities(self.grid)
                collapse((4,4), self.grid)

            scale = 54
            for i in range(int(self.screen.get_height()/scale)):
                for j in range(int(self.screen.get_width()/scale)):
                    self.grid[i][j].draw()

            time = self.clock.tick() / 1000
            pygame.display.flip()