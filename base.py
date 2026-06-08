from abc import ABC, abstractmethod
import pygame
import random as r


class Entity(ABC):
    def __init__(self, pos: pygame.Vector2):
        self.pos = pos

    def __hash__(self):
        return id(self)

    @abstractmethod
    def habit(self) -> list["Behaves"]: ...

    @abstractmethod
    def surface(self) -> pygame.Surface | None: ...

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__.items()})"


class World:
    def __init__(self):
        self.entity_map: dict["Entity", pygame.Vector2] = dict()
        self.grass_map = [
            [Grass(r.randint(70, 100)) for _ in range(16)] for _ in range(10)
        ]

    @property
    def entities(self) -> list[Entity]:
        return list(self.entity_map.keys())

    def summon(self, entity, pos):
        ett = entity(*entity.info(), pos, self)
        self.entity_map[ett] = pos
        if isinstance(ett,Animal):
            addlog(f'새로운 {ett.name}을(를) 소환했습니다.')

    def update(self):
        for entity in self.entities:
            for a in entity.habit():
                if a.act(self):
                    break

    def remove(self, entity: "Entity"):
        del self.entity_map[entity]

    def findtarget(self, entity: "Entity", targetlist=None, findrange=float("inf")):
        return [
            an
            for an in self.entities
            if (targetlist is None or isinstance(an, targetlist))
            and (an.pos.distance_to(entity.pos)) <= findrange
        ]

    def findnearesttarget(self, entity:Entity, targetlist=None, findrange=float("inf"))->Entity|None:
        targets = self.findtarget(entity, targetlist, findrange)
        if len(targets) == 0:
            return None
        return min(targets, key=lambda aa: aa.pos.distance_to(entity.pos))
    
    def wheregrass(self,entity):
        return (entity.pos.x//75,entity.pos.y//75)


class Behaves(ABC):
    @abstractmethod
    def act(self, world: "World") -> bool: ...


class Animal(Entity):
    MAXHUNGER=50
    def __init__(
        self,
        name,
        hp,
        attack,
        defense,
        hunger,
        speed,
        sight: float,
        pos: pygame.Vector2,
        world,
    ):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.hunger = hunger
        self.speed = speed
        self.sight = sight
        self.pos = pos
        self.world = world
        
    @property
    def hunger(self):
        return self._hunger
    @hunger.setter
    def hunger(self,v):
        self._hunger=v if v<=self.MAXHUNGER else self.MAXHUNGER


    def move(self, speed, goto: pygame.Vector2):
        self.pos = goto
        if speed > self.speed:
            self.hunger -= 0.05
        self.world.entity_map[self]=goto
        return f"{self.name}이 {goto.x},{goto.y}로 이동"

    def dead(self):
        self.world.summon(Carcass, self.pos)
        self.world.remove(self)
        addlog(f'{self.name}이 사망했습니다.')


class Carcass(Entity):
    def __init__(self, remain: float, pos: "pygame.Vector2", world):
        self.remain = remain
        self.pos = pos

    @classmethod
    def info(cls):
        return (10,)

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


class Grass:
    def __init__(self, remain):
        self.remain = remain

    def grow(self, val):
        self.remain += val

def addlog(txt):
    with open('log.txt','a',encoding='UTF-8') as f:
        f.write(txt+'\n')