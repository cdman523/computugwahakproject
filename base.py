from abc import ABC, abstractmethod
from geo import Vector


class Entity(ABC):
    def __hash__(self):
        return id(self)

    @abstractmethod
    def habit(self) -> list["Behaves"]: ...


class World:
    def __init__(self):
        self.entity_map = dict()

    @property
    def animals(self):
        return list(self.entity_map.keys())

    def update(self):
        for animal in self.animals:
            for a in animal.habit():
                if a.act():
                    break

    def remove(self, entity: "Entity"):
        del self.entity_map[entity]


class Behaves(ABC):
    @abstractmethod
    def act(self, entity: "Entity", world: "World") -> bool: ...


class Animal(Entity):
    def __init__(
        self, name, hp, attack, defense, hunger, speed, sight: float, pos: Vector
    ):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.hunger = hunger
        self.speed = speed
        self.sight = sight
        self.pos = pos

    @abstractmethod
    def move(self) -> None: ...
