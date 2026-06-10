from base import Animal
import pygame
from behaves import *
import random as r


# 예시 동물
class ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA(
    Animal
):
    ENUM=0
    IMAGE=pygame.image.load("images/testimage0.png")
    def habit(self):
        return [EXAMPLE_JUMPING(self, 10), EXAMPLE_WALK(self), EXAMPLE_HELLO(self)]

    def surface(self):
        return pygame.transform.scale(self.IMAGE, (60, 60))

    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f"대서우{cls.ENUM}", 10,10,10,20,10,10)


def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

class Buffalo(Animal):
    ENUM = 0
    IMAGE=pygame.image.load("images/bufalo.png")
    @classmethod
    def info(cls):
        cls.ENUM += 1
        # 기준 스탯: HP 350, ATK 38, DEF 70, Hunger 20, SPD 3, Sight 130
        hp = int(round(clamp(r.gauss(350, 15), 300, 400)))
        attack = int(round(clamp(r.gauss(38, 3), 28, 48)))
        defense = int(round(clamp(r.gauss(70, 5), 55, 85)))
        hunger = 20
        speed = round(clamp(r.gauss(3.0, 0.2), 2.0, 4.0), 2)
        sight = int(round(clamp(r.gauss(130, 10), 100, 160)))
        
        return (f"버팔로{cls.ENUM}", hp, attack, defense, hunger, speed, sight)

    def habit(self):
        return [CHARGE_RUSH(self), BUFFALO_MOVE_TO_BUFFALO(self),EAT_GRASS(self,0.4), WANDER(self)]

    def surface(self):
        return pygame.transform.scale(
            self.IMAGE, (75,75)
        )


class Gazelle(Animal):
    ENUM = 0
    IMAGE=pygame.image.load("images/gazel.png")
    @classmethod
    def info(cls):
        cls.ENUM += 1
        # 기준 스탯: HP 80, ATK 8, DEF 15, Hunger 20, SPD 6, Sight 110
        hp = int(round(clamp(r.gauss(80, 5), 65, 95)))
        attack = int(round(clamp(r.gauss(8, 1), 5, 11)))
        defense = int(round(clamp(r.gauss(15, 2), 10, 20)))
        hunger = 20
        speed = round(clamp(r.gauss(6.0, 0.4), 4.5, 7.5), 2)
        sight = int(round(clamp(r.gauss(110, 8), 90, 130)))
        
        return (f"가젤{cls.ENUM}", hp, attack, defense, hunger, speed, sight)

    def habit(self):
        return [GAZELLE_MOVE_TO_GAZELLE(self),EAT_GRASS(self,0.2), WANDER(self)]

    def surface(self):
        return pygame.transform.scale(
            self.IMAGE, (60,60)
        )


class Hyena(Animal):
    ENUM = 0
    IMAGE=pygame.image.load("images/hyena.png")
    @classmethod
    def info(cls):
        cls.ENUM += 1
        # 기준 스탯: HP 120, ATK 30, DEF 25, Hunger 60, SPD 4, Sight 140
        hp = int(round(clamp(r.gauss(120, 8), 100, 140)))
        attack = int(round(clamp(r.gauss(30, 2), 24, 36)))
        defense = int(round(clamp(r.gauss(25, 2), 19, 31)))
        hunger = 60
        speed = round(clamp(r.gauss(4.0, 0.2), 3.0, 5.0), 2)
        sight = int(round(clamp(r.gauss(140, 10), 110, 170)))
        
        return (f"하이에나{cls.ENUM}", hp, attack, defense, hunger, speed, sight)

    def habit(self):
        return [ATTACK_TARGET(self, [Gazelle, Zebra]), EAT_CARCASS(self), ATTACK_LION_WHEN_MANY(self), WANDER(self)]
    
    def surface(self):
        return pygame.transform.scale(
            self.IMAGE, (60,60)
        )


class Lion(Animal):
    ENUM = 0
    IMAGE=pygame.image.load("images/lion0.png")
    @classmethod
    def info(cls):
        cls.ENUM += 1
        # 기준 스탯: HP 300, ATK 40, DEF 50, Hunger 50, SPD 4, Sight 150
        hp = int(round(clamp(r.gauss(300, 10), 250, 400)))
        attack = int(round(clamp(r.gauss(40, 3), 30, 50)))
        defense = int(round(clamp(r.gauss(50, 4), 40, 60)))
        hunger = 50
        speed = round(clamp(r.gauss(5.0, 0.2), 3.0, 6.0), 2)
        sight = int(round(clamp(r.gauss(150, 10), 120, 180)))
        
        return (f"사자{cls.ENUM}", hp, attack, defense, hunger, speed, sight)

    def habit(self):
        return [
            LION_REST(self),
            EAT_CARCASS(self),
            LION_GUARD_CARCASS(self),
            LION_HUNT_PACK(self),
            ATTACK_TARGET(self, [Zebra, Gazelle]),
            WANDER(self)
        ]

    def surface(self):
        return pygame.transform.scale(
            self.IMAGE, (75,75)
        )


class Zebra(Animal):
    ENUM = 0
    IMAGE=pygame.image.load("images/zebra.png")
    @classmethod
    def info(cls):
        cls.ENUM += 1
        # 기준 스탯: HP 130, ATK 20, DEF 30, Hunger 25, SPD 5, Sight 200
        hp = int(round(clamp(r.gauss(130, 7), 110, 150)))
        attack = int(round(clamp(r.gauss(20, 2), 15, 25)))
        defense = int(round(clamp(r.gauss(30, 3), 20, 40)))
        hunger = 25
        speed = round(clamp(r.gauss(4.5, 0.3), 4.0, 6.0), 2)
        sight = int(round(clamp(r.gauss(200, 15), 160, 240)))
        
        return (f"얼룩말{cls.ENUM}", hp, attack, defense, hunger, speed, sight)

    def habit(self):
        return [
            ZEBRA_ALERT(self),
            RUNAWAY(self),
            EAT_GRASS(self,0.2),
            WANDER(self)
        ]

    def surface(self):
        return pygame.transform.scale(
            self.IMAGE, (60,60)
        )


class Elephant(Animal):
    ENUM = 0
    IMAGE=pygame.image.load('images/alephant.png')
    @classmethod
    def info(cls):
        cls.ENUM += 1
        # 기준 스탯: HP 700, ATK 55, DEF 120, Hunger 20, SPD 2, Sight 120
        hp = int(round(clamp(r.gauss(700, 30), 600, 800)))
        attack = int(round(clamp(r.gauss(55, 4), 45, 65)))
        defense = int(round(clamp(r.gauss(120, 8), 95, 145)))
        hunger = 20
        speed = round(clamp(r.gauss(2.0, 0.1), 1.5, 2.5), 2)
        sight = int(round(clamp(r.gauss(120, 8), 90, 150)))
        
        return (f"코끼리{cls.ENUM}", hp, attack, defense, hunger, speed, sight)

    def habit(self):
        return [EAT_GRASS(self,1.0),WANDER(self)]

    def surface(self):
        return pygame.transform.scale(
            self.IMAGE, (100,100)
        )
