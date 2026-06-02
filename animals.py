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
        return pygame.transform.scale(pygame.image.load("images/images.jpeg"), (60, 60))

    @classmethod
    def info(cls):
        return ("대서우", 10, 10, 10, 10, 10, 10)
=======
class Buffalo(Animal):
    def habit(self):
        return [CHARGE_RUSH(self), BUFFALO_MOVE_TO_BUFFALO(self)]

class Gazelle(Animal):
    def habit(self):
        return [GAZELLE_MOVE_TO_GAZELLE(self)]
    
>>>>>>> 6357cfc6e4cb93c348519f406b4e86b57a0e04e9
