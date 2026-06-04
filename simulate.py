# 시각화 코드
import pygame
from base import World, Carcass
from animals import (
    ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA,
)
import random as r


class Simulator:
    SCREEN_H, SCREEN_W = 1200, 750

    def __init__(self):
        pygame.init()
        self.world = World()
        self.running = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_H, self.SCREEN_W))
        self.world.summon(
            ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA,
            pygame.Vector2(40, 100),
        )

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.world.summon(
                        ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA,
                        pygame.Vector2(pygame.mouse.get_pos()),
                    )

    def draw_background(self):
        self.screen.blit(
            pygame.transform.scale(
                pygame.image.load("images/bg1.png"),
                (self.SCREEN_H, self.SCREEN_W),
            ),
            (0, 0),
        )

    def draw_entities(self):
        for e, loc in self.world.entity_map.items():
            surface = e.surface()
            if surface is None:
                continue
            self.screen.blit(surface, loc)
