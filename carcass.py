from base import Entity, Behaves, World


class Carcass(Entity):
    def __init__(self, remain: int):
        self.remain = remain

    def habit(self) -> list["Behaves"]:
        return [Rot()]


class Rot(Behaves):
    ROT_VELOCITY = 10

    def act(self, entity: Entity, world: World) -> bool:
        if not isinstance(entity, Carcass):
            return False

        if entity.remain <= 0:
            world.remove(entity)
        else:
            entity.remain -= self.ROT_VELOCITY

        return True
