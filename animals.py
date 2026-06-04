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


class Buffalo(Animal):
    def habit(self):
        return [CHARGE_RUSH(self), BUFFALO_MOVE_TO_BUFFALO(self)]


class Gazelle(Animal):
    def habit(self):
        return [GAZELLE_MOVE_TO_GAZELLE(self)]

class hyena(Animal):
    def habit(self):
        return [EXAMPLE_JUMPING(self, 10), EXAMPLE_WALK(self)]

    def info(self):
        return

class LION_REST(Behaves):
    """
    배가 부른 사자는 초식동물이 곁을 지나가도 사냥하지 않고 휴식한다.
    hunger가 max_hunger의 80% 이상이면 아무것도 하지 않고 True 반환.
    (ATTACK_TARGET보다 habit 리스트 앞에 두어 사냥을 막는다)
    """
    def __init__(self, actor: Animal):
        self.actor = actor
 
    def act(self, world: World):
        if self.actor.hunger < self.actor.max_hunger * 0.8:
            return False  # 배고프면 휴식 불가 → 다음 행동으로 넘김
        # 배부름 → 제자리 대기
        return True
