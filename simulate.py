# 시각화 코드
import pygame
from base import World, Carcass, addlog
from animals import *
import random as r


class Simulator:
    SCREEN_H, SCREEN_W = 1200, 750

    def __init__(self):
        pygame.init()
        self.world = World()
        self.running = False
        self.clock = pygame.time.Clock()
        self.xspeed=1
        self.timecount=0
        self.pause=False
        with open('log.txt','w',encoding='utf-8'):pass
        pygame.display.set_caption('서우의 ALEPHANT 프로젝트')
        self.screen = pygame.display.set_mode((self.SCREEN_H, self.SCREEN_W))
        self.world.summon(
            ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA,
            pygame.Vector2(40, 100),
        )

    def run(self):
        self.running = True
        while self.running:
            self.handle_user_input()
            self.timecount+=self.xspeed*(not self.pause)
            while self.timecount>=1:
                self.world.update()
                self.timecount-=1
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self):
        self.draw_background()
        self.draw_entities()
        self.draw_UI()

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                mousepos=pygame.Vector2(pygame.mouse.get_pos())
                if event.key == pygame.K_0:
                    self.world.summon(
                        ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA,
                        mousepos,
                    )
                elif event.key==pygame.K_1:
                    self.world.summon(Elephant,mousepos)
                elif event.key==pygame.K_2:
                    self.world.summon(Lion,mousepos)
                elif event.key==pygame.K_3:
                    self.world.summon(Hyena,mousepos)
                elif event.key==pygame.K_4:
                    self.world.summon(Buffalo,mousepos)
                elif event.key==pygame.K_5:
                    self.world.summon(Zebra,mousepos)
                elif event.key==pygame.K_6:
                    self.world.summon(Gazelle,mousepos)
                elif event.key==pygame.K_SPACE:
                    self.pause=not self.pause
                elif event.key==pygame.K_UP:
                    self.xspeed+=0.1
                elif event.key==pygame.K_DOWN:
                    self.xspeed-=0.1
                elif event.key==pygame.K_RIGHT:
                    self.xspeed+=1
                elif event.key==pygame.K_LEFT:
                    self.xspeed-=1
                elif event.key==pygame.K_z:
                    print(self.world.entities)
    def draw_background(self):
        self.screen.blit(
            pygame.transform.scale(
                pygame.image.load("images/gbg1.png"),
                (self.SCREEN_H, self.SCREEN_W),
            ),
            (0, 0),
        )

    def draw_entities(self):
        for e, loc in self.world.entity_map.items():
            surface = e.surface()
            if surface is None:
                continue
            if isinstance(e,Animal):
                self.draw_hpbar(e,loc,surface)
            self.screen.blit(surface, loc)
    
    def draw_hpbar(self,entity,pos,surface):
        width=surface.get_width()
        height=6
        hp_ratio=max(0,min(1,entity.hp/entity.maxhp))
        x=pos.x
        y=pos.y-10
        pygame.draw.rect(
        self.screen,
        (80, 80, 80),
        (x, y, width, height)
        )

        # 체력
        pygame.draw.rect(
        self.screen,
        (0, 255, 0),
        (x, y, width * hp_ratio, height)
        )

        # 테두리
        pygame.draw.rect(
        self.screen,
        (255, 255, 255),
        (x, y, width, height),
        1
        )

    @staticmethod
    def draw_text(screen,text,x,y,size,color=(255,255,255)):
        font = pygame.font.SysFont('malgungothic', size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_UI(self):
        self.draw_text(self.screen,f'{self.xspeed:.2f}배속'+('(일시정지됨)' if self.pause else ''),0,0,30)