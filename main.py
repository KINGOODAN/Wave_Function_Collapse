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

    def run(self):
        
        self.grid = makeGrid(self.screen, self.grid)
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            if keys[pygame.K_LSHIFT]:
                self.grid = makeGrid(self.screen, self.grid)

            self.screen.fill((0,0,0))

            if not self.done: #type: ignore
                self.done,self.grid = determine_possibilities(self.grid)
                self.grid = collapse((4,4), self.grid)

            scale = 54
            for i in range(int(self.screen.get_height()/scale)):
                for j in range(int(self.screen.get_width()/scale)):
                    self.grid[i][j].draw()

            time = self.clock.tick() / 1000
            pygame.display.flip()