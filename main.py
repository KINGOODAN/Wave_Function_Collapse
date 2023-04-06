import pygame
from tile import Tile, Slot, makeGrid, determine_possibilities, collapse


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.grid:list[list[Slot]] = []
        self.done:bool = False
        self.tile_size:int = 60
        self.img_tile_dimentions:tuple[int,int] = (4,4)

    def run(self):
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