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
        self.grass_surface=None
        self.font=pygame.font.SysFont('malgungothic',16)
        self.logpoint=0
        self.game_surface = pygame.Surface((1200, 750), pygame.SRCALPHA)
        self.hover=None
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
        self.hv=self.get_hovered_animal()
        self.hover=self.hv if self.hv is not None else self.hover
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
                    with open('log.txt','r',encoding='utf-8') as f:
                        self.logpoint=len(f.readlines())
                elif event.key==pygame.K_SLASH:
                    print(self.world.entities)
                elif event.key==pygame.K_c:
                    self.grassmap=not self.grassmap
                elif event.key==pygame.K_ESCAPE:
                    self.running=False
            if event.type==pygame.MOUSEWHEEL:
                if event.y>0:
                    self.xspeed+=0.5
                elif event.y<0:
                    self.xspeed=max(self.xspeed-0.5,0.1)
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

    def draw_text(self,screen,text,x,y,size,color=(255,255,255)):
        font = pygame.font.SysFont('malgungothic', size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_UI(self):
        self.draw_text(self.screen,f'[{self.world.worldtime//3600:02}:{self.world.worldtime%3600//60:02}] {self.xspeed:.2f}배속'+('(일시정지됨)' if self.pause else ''),10,self.fullSCREEN_W-50,30)
        if self.grassmap:
            self.update_grassmap()
            self.screen.blit(
                self.grass_surface,
                (0,0)
            )
        self.draw_text(self.screen,'[esc] 종료 [space] 일시정지 [z] NUCLEAR [x] 로그 지우기 [c] 풀 보이기',0,750,20)
        self.draw_text(self.screen,'[1] Elephant [2] Lion [3] Hyena [4] Buffalo [5] Zebra [6] Gazelle [7] Carcass',0,780,20)
        self.draw_text(self.screen,'[↑] +0.1배속 [↓] -0.1배속 [→] +1배속 [←] -1배속 [마우스 휠] ±0.5배속씩 조정',0,810,20)
        if self.hover is not None:
            self.draw_text(self.screen,f'이름 {self.hover.name} 종 {self.hover.__class__.__name__}',750,750,20)
            self.draw_text(self.screen,f'체력 {self.hover.hp:.0f}/{self.hover.maxhp:.0f} 배고픔 {self.hover.hunger:.0f}/{self.hover.MAXHUNGER:.0f}',750,780,20)
            self.draw_text(self.screen,f'속도 {self.hover.speed:.1f} 공격력 {self.hover.attack} 방어력{self.hover.defense} 시야 {self.hover.sight}',750,810,20)
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

        for paragraph in text.split("\n")[self.logpoint:]:

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
    def update_grassmap(self):
        self.grass_surface = pygame.Surface(
        (1200, 750),
        pygame.SRCALPHA
    )

        for y in range(10):
            for x in range(16):

                grass = self.world.grass_map[y][x]

                value = round(grass.remain,2)

                ratio = max(
                    0,
                    min(value / 20, 1)
                )

                # 빨강 -> 노랑 -> 초록
                color = (
                    int(255 * (1 - ratio)),
                    int(255 * ratio),
                    0,
                    100
                )

                rect = pygame.Rect(
                    x * 75,
                    y * 75,
                    75,
                    75
                )   

                pygame.draw.rect(
                    self.grass_surface,
                    color,
                    rect
                )

                pygame.draw.rect(
                    self.grass_surface,
                    (50,50,50),
                    rect,
                    1
                )

                text = self.font.render(
                    f'{value:.2f}',
                    True,
                    (255,255,255)
                )

                text_rect = text.get_rect(
                    center=rect.center
                )

                self.grass_surface.blit(
                    text,
                    text_rect
                )
    def get_hovered_animal(self):
        mouse_pos = pygame.mouse.get_pos()

        for entity, pos in reversed(
            sorted(
                self.world.entity_map.items(),
                key=lambda item: item[0].layer
            )
        ):
            if not isinstance(entity, Animal):
                continue

            surface = entity.surface()
            rect = surface.get_rect(center=pos)

            if rect.collidepoint(mouse_pos):
                return entity

        return None