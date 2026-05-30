from base import Entity, Behaves, World
import pygame


class Carcass(Entity):
    def __init__(self, remain: float, pos: "pygame.Vector2"):
        self.remain = remain
        self.pos = pos

    def habit(self) -> list["Behaves"]:
        return [Rot(self)]

    def surface(self):
        sf = pygame.transform.scale(
            pygame.image.load("images/testimage0.png"), (60, 60)
        )
        sf.set_alpha(int(self.remain * 255 / 10))
        return sf


class Rot(Behaves):
    ROT_VELOCITY = 0.05

    def __init__(self, carcass: Carcass):
        self.carcass = carcass

    def act(self, world: World) -> bool:
        if self.carcass.remain <= 0:
            world.remove(self.carcass)
        else:
            self.carcass.remain -= self.ROT_VELOCITY

        return True
