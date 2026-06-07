from base import Animal
import pygame
from behaves import *


# 예시 동물
class ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA(
    Animal
):
    def habit(self):
        return [EXAMPLE_JUMPING(self, 10), EXAMPLE_WALK(self), EXAMPLE_HELLO(self)]

    def surface(self):
        return pygame.transform.scale(pygame.image.load("images/bufalo.png"), (60, 60))

    @classmethod
    def info(cls):
        return ("대서우", 10,10,10,20,10,10)


class Buffalo(Animal):
    ENUM=0

    def habit(self):
        return [CHARGE_RUSH(self), BUFFALO_MOVE_TO_BUFFALO(self)]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/bufalo.png"), (60, 60)
        )

    @classmethod
    def info(cls):
        cls.ENUM+=1
        pass

class Gazelle(Animal):
    def habit(self):
        return [GAZELLE_MOVE_TO_GAZELLE(self)]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/gazel.png"), (60, 60)
        )

    @classmethod
    def info(cls):
        cls.ENUM+=1
        pass

class Hyena(Animal):
    def habit(self):
        return [ATTACK_TARGET(self), EAT_CARCASS(self)]
    
    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/hyena.png"), (60, 60)
        )
    
    @classmethod
    def info(cls):
        cls.ENUM+=1
        pass

class Lion(Animal):
    ENUM=0

    @classmethod
    def info(cls):
        # (name, hp, attack, defense, hunger, speed, sight)
        cls.ENUM+=1
        return (f"Lion{cls.ENUM}", 200, 40, 10, 80, 4, 150)

    def habit(self):
        return [
            LION_REST(self),
            LION_GUARD_CARCASS(self),
            LION_HUNT_PACK(self),
            ATTACK_TARGET(self, [Zebra, Gazelle]),
        ]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/lion0.png"), (60, 60)
        )


class Zebra(Animal):
    ENUM=0

    @classmethod
    def info(cls):
        return (f"Zebra{cls.ENUM}", 80, 5, 5, 80, 5, 200)  # sight가 Lion보다 넓음

    def habit(self):
        return [
            ZEBRA_ALERT(self),
            RUNAWAY(self),
        ]

    def surface(self):
        return pygame.transform.scale(
            pygame.image.load("images/zebra.png"), (60, 60)
        )