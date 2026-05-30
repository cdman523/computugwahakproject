# 시각화 코드
import pygame
from base import World
from carcass import Carcass


class Simulator:
    SCREEN_H, SCREEN_W = 800, 600

    def __init__(self):
        pygame.init()
        self.world = World()
        self.running = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_H, self.SCREEN_W))
        self.world.entity_map[Carcass(10)] = pygame.Vector2(40, 80)

    def run(self):
        self.running = True
        while self.running:
            self.handle_user_input()
            self.world.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self):
        self.draw_background()
        self.draw_entities()

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw_background(self):
        self.screen.blit(pygame.image.load("images/background.png"), (0, 0))

    def draw_entities(self):
        for e, loc in self.world.entity_map.items():
            surface = e.surface()
            if surface is None:
                continue
            self.screen.blit(surface, loc)
