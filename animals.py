from base import Animal
import pygame
from behaves import *


# 예시 동물
class ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA(
    Animal
):
    ENUM=0
    def habit(self):
        return [EXAMPLE_JUMPING(self, 10), EXAMPLE_WALK(self), EXAMPLE_HELLO(self)]

    def surface(self):
        return pygame.transform.scale(pygame.image.load("images/bufalo.png"), (60, 60))

    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f"대서우{cls.ENUM}", 10,10,10,20,10,10)


class Buffalo(Animal):
    ENUM=0

    def habit(self):
        return [CHARGE_RUSH(self), BUFFALO_MOVE_TO_BUFFALO(self),WANDER(self)]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/bufalo.png"), (60, 60)
        )
    def info(cls):
        cls.ENUM += 1
        return (f"물소{cls.ENUM}", 350, 38, 70, 20, 3, 130)
    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f'버팔로{cls.ENUM}',)

class Gazelle(Animal):
    ENUM=0
    def habit(self):
        return [GAZELLE_MOVE_TO_GAZELLE(self),WANDER(self)]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/gazel.png"), (60, 60)
        )
    def info(cls):
        cls.ENUM += 1
        return (f"가젤{cls.ENUM}", 80, 8, 15, 20, 6, 110)
    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f'가젤{cls.ENUM}',)

class Hyena(Animal):
    ENUM=0
    def habit(self):
        return [ATTACK_TARGET(self,[Gazelle,Zebra]), EAT_CARCASS(self), ATTACK_LION_WHEN_MANY(self),WANDER(self)]
    
    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/hyena.png"), (60, 60)
        )
    def info(cls):
        cls.ENUM += 1
        return (f"하이에나{cls.ENUM}", 120, 30, 25, 60, 4, 140)

    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f'하이에나{cls.ENUM}',)


class Lion(Animal):
    ENUM=0
    @classmethod
    def info(cls):
        # (name, hp, attack, defense, hunger, speed, sight)
        cls.ENUM+=1
        return (f"사자{cls.ENUM}", 200, 40, 50, 50, 4, 150)

    def habit(self):
        return [
            LION_REST(self),
            EAT_CARCASS(self),
            LION_GUARD_CARCASS(self),
            LION_HUNT_PACK(self),
            ATTACK_TARGET(self, [Zebra, Gazelle]),
            DONOTHING(self),
            WANDER(self)
        ]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/lion0.png"), (60, 60)
        )


class Zebra(Animal):
    ENUM=0

    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f"얼룩말{cls.ENUM}", 130, 20, 30, 25, 5, 200)  # sight가 Lion보다 넓음

    def habit(self):
        return [
            ZEBRA_ALERT(self),
            RUNAWAY(self),
            EAT_GRASS(self),
            DONOTHING(self),
            WANDER(self)
        ]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/zebra.png"), (60, 60)
        )
    
class Elephant(Animal):
    ENUM=0
    @classmethod
    def info(cls):
        cls.ENUM+=1
        return (f'Alephant{cls.ENUM}',)
    def habit(self):
        return [WANDER(self)]
    def surface(self):
        return pygame.transform.scale(pygame.image.load('images/alephant.png'),(60,60))
    def info(cls):
        cls.ENUM += 1
        return (f"코끼리{cls.ENUM}", 700, 55, 120, 20, 2, 120)
