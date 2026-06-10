# 시각화 코드
import pygame
from base import World, Carcass, addlog
from animals import *
import random as r


class Simulator:
    SCREEN_H, SCREEN_W = 1200, 750

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()

        self.fullSCREEN_H = info.current_w
        self.fullSCREEN_W = info.current_h
        self.world = World()
        self.running = False
        self.clock = pygame.time.Clock()
        self.xspeed=1
        self.timecount=0
        self.pause=False
        self.grassmap=False
        self.game_surface = pygame.Surface((1200, 750), pygame.SRCALPHA)
        with open('log.txt','w',encoding='utf-8'):pass
        pygame.display.set_caption('서우의 ALEPHANT 프로젝트')
        self.screen = pygame.display.set_mode((self.fullSCREEN_H,self.fullSCREEN_W))

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
        self.draw_log()

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                mousepos=pygame.Vector2(pygame.mouse.get_pos())
                cansummon=0<mousepos.x<self.SCREEN_H and 0<mousepos.y<self.SCREEN_W
                if event.key == pygame.K_0 and cansummon:
                    self.world.summon(
                        ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA,
                        mousepos,
                    )
                elif event.key==pygame.K_1 and cansummon:
                    self.world.summon(Elephant,mousepos)
                elif event.key==pygame.K_2 and cansummon:
                    self.world.summon(Lion,mousepos)
                elif event.key==pygame.K_3 and cansummon:
                    self.world.summon(Hyena,mousepos)
                elif event.key==pygame.K_4 and cansummon:
                    self.world.summon(Buffalo,mousepos)
                elif event.key==pygame.K_5 and cansummon:
                    self.world.summon(Zebra,mousepos)
                elif event.key==pygame.K_6 and cansummon:
                    self.world.summon(Gazelle,mousepos)
                elif event.key==pygame.K_7 and cansummon:
                    self.world.summon(Carcass,mousepos)
                elif event.key==pygame.K_SPACE:
                    self.pause=not self.pause
                elif event.key==pygame.K_UP:
                    self.xspeed+=0.1
                elif event.key==pygame.K_DOWN:
                    self.xspeed-=0.1
                    if self.xspeed<=0:
                        self.xspeed=0.1
                elif event.key==pygame.K_RIGHT:
                    self.xspeed+=1
                elif event.key==pygame.K_LEFT:
                    self.xspeed-=1
                    if self.xspeed<=0:
                        self.xspeed=0.1
                elif event.key==pygame.K_z and cansummon:
                    self.world.summon(Nuclear,mousepos)
                elif event.key==pygame.K_x:
                    pass
                elif event.key==pygame.K_SLASH:
                    print(self.world.entities)
                elif event.key==pygame.K_c:
                    self.grassmap=not self.grassmap
                elif event.key==pygame.K_ESCAPE:
                    self.running=False
    def draw_background(self):
        self.screen.fill((80,80,80))
        self.screen.blit(
            pygame.transform.scale(
                pygame.image.load("images/gbg1.png"),
                (self.SCREEN_H, self.SCREEN_W),
            ),
            (0, 0),
        )

    def draw_entities(self):
        self.game_surface.fill((0, 0, 0, 0))
        for e, loc in sorted(self.world.entity_map.items(),key=lambda item:item[0].layer):
            surface = e.surface()
            if surface is None:
                continue
            rect=surface.get_rect(center=loc-pygame.Vector2(0,e.radius*0.3)) if isinstance(e,Explosion) else surface.get_rect(center=loc)
            self.game_surface.blit(surface, rect)
            if isinstance(e,Animal):
                self.draw_bar(e,loc,e.surface())  
        self.screen.blit(self.game_surface,(0,0))
    
    def draw_bar(self,entity,pos,surface):
        rect = surface.get_rect(center=pos)
        width=rect.width
        height=6
        x=rect.left
        y=rect.top-15
        hpratio=entity.hp/entity.maxhp
        hungerratio=entity.hunger/entity.MAXHUNGER
        pygame.draw.rect(
        self.game_surface,
        (40, 40, 40),
        (x, y, width, height)
        )

        # 체력
        pygame.draw.rect(
        self.game_surface,
        (255,255,0) if hpratio>0.6 else (255,165,0) if hpratio>0.3 else (255,99,71),
        (x, y, width * hpratio, height)
        )

        # 테두리
        pygame.draw.rect(
        self.game_surface,
        (255, 255, 255),
        (x, y, width, height),
        1
        )

        pygame.draw.rect(
        self.game_surface,
        (40, 40, 40),
        (x, y+8, width, height)
        )

        # 체력
        pygame.draw.rect(
        self.game_surface,
        (160, 110, 60),
        (x, y+8, width * hungerratio, height)
        )

        # 테두리
        pygame.draw.rect(
        self.game_surface,
        (255, 255, 255),
        (x, y+8, width, height),
        1
        )

        self.screen.blit(self.game_surface,(0,0))

    @staticmethod
    def draw_text(screen,text,x,y,size,color=(255,255,255)):
        font = pygame.font.SysFont('malgungothic', size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_UI(self):
        self.draw_text(self.screen,f'{self.xspeed:.2f}배속'+('(일시정지됨)' if self.pause else ''),0,0,30)
        if self.grassmap:
            CELL_SIZE = 75

            for y in range(10):
                for x in range(16):

                    rect = pygame.Rect(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )

                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 100),
                        rect,
                        1
                    )
                                   
                    self.draw_text(
                        self.screen,
                        f'{self.world.grass_map[y][x].remain:.2f}',
                        rect.x + CELL_SIZE/2-10,
                        rect.y + CELL_SIZE/2-10,
                        10
                    )
    def draw_log(self):

        # 로그창 영역

        log_x = self.SCREEN_H + 10
        log_y = 0

        log_w = self.fullSCREEN_H - self.SCREEN_H - 20
        log_h = self.fullSCREEN_W

        # 배경
        pygame.draw.rect(
            self.screen,
            (25, 25, 25),
            (log_x, log_y, log_w, log_h)
        )

        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            (log_x, log_y, log_w, log_h),
            2
        )

        font = pygame.font.SysFont(
            "malgungothic",
            12
        )

        # 로그 읽기
        try:
            with open(
                "log.txt",
                "r",
                encoding="utf-8"
            ) as f:
                text = f.read()

        except FileNotFoundError:
            text = ""

        # 줄바꿈 처리
        lines = []

        for paragraph in text.split("\n"):

            if paragraph == "":
                lines.append("")
                continue

            current = ""

            for word in paragraph.split():

                test = (
                    current + " " + word
                    if current
                    else word
                )

                if font.size(test)[0] < log_w - 10:
                    current = test

                else:
                    lines.append(current)
                    current = word

            lines.append(current)

        # 표시 가능한 줄 수
        line_height = font.get_linesize()

        max_lines = log_h // line_height

        # 자동 스크롤
        if len(lines) > max_lines:
            lines = lines[-max_lines:]

        # 출력
        for i, line in enumerate(lines):

            surface = font.render(
                line,
                True,
                (220, 220, 220)
            )

            self.screen.blit(
                surface,
                (
                    log_x + 5,
                    log_y + i * line_height
                )
            )