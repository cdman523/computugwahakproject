from base import Animal
from pygame import Vector2
from behaves import *


# 예시 동물
class ALEPHANT_THE_LEGEND_ANIMAL_IS_BY_SUWOO_MOONSUWOO_GU_NEN_GA_HI_SIN_HWA_LA_GO_HAL_SOO_IT_DA(
    Animal
):
    def habit(self):
        return [EXAMPLE_JUMPING(self, 10), EXAMPLE_WALK(self), EXAMPLE_HELLO(self)]
