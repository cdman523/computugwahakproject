from base import Entity, Behaves, World
import pygame


class Carcass(Entity):
    def __init__(self, remain: int):
        self.remain = remain

    def habit(self) -> list["Behaves"]:
        return [Rot(self)]

    def surface(self):
        return pygame.image.load("images/images.jpeg")


class Rot(Behaves):
    ROT_VELOCITY = 0

    def __init__(self, carcass: Carcass):
        self.carcass = carcass

    def act(self, world: World) -> bool:
        if self.carcass.remain <= 0:
            world.remove(self.carcass)
        else:
            self.carcass.remain -= self.ROT_VELOCITY

        return True
