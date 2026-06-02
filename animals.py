from base import Animal
from pygame import Vector2
from behaves import *


# 예시 동물
class ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA(
    Animal
):
    def habit(self):
        return [EXAMPLE_JUMPING(self, 10), EXAMPLE_WALK(self), EXAMPLE_HELLO(self)]

class Buffalo(Animal):
    def habit(self):
        return [CHARGE_RUSH(self), BUFFALO_MOVE_TO_BUFFALO(self)]

class Gazelle(Animal):
    def habit(self):
        return [GAZELLE_MOVE_TO_GAZELLE(self)]
    
