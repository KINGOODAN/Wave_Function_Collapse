import pygame
from tile import Tile


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.template = pygame.image.load("test_image.png")
        self.tile = Tile(self.template,3,3,(100,100))

    def run(self):
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            while keys[pygame.K_LSHIFT]:
                pygame.event.get()
                keys = pygame.key.get_pressed()
                self.screen.fill((0, 0, 0))
                pygame.display.flip()

            time = self.clock.tick() / 1000
            pygame.display.flip()