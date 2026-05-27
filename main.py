from abc import *
import random as r
import math as m
from behaves import *

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __sub__(self, v2):
        return self + v2 * (-1)

    def __truediv__(self, v2):
        return self * (1 / v2)

    def __eq__(self, v2):
        return (self.x, self.y) == (v2.x, v2.y)

    def angVec(r, theta):
        return Vector(m.cos(m.radians(theta)), m.sin(m.radians(theta))) * r

    def __abs__(self):
        return m.hypot(self.x, self.y)

    @property
    def angle(self):
        return m.degrees(m.atan2(self.y, self.x))

    
class Animal():
    def __init__(self,name,hp,attack,defense,hunger,speed,sight,pos):
        self.name=name
        self.hp=hp
        self.attack=attack
        self.defense=defense
        self.hunger=hunger
        self.speed=speed
        self.sight=sight
        self.pos=pos
    def move():
        pass
    @abstractmethod
    def habit():
        pass

class World():
    def __init__(self):
        self.animal_map=dict()
    @property
    def animals(self):
        return list(self.animal_map.keys())
    def update(self):
        for animal in self.animals:
            for a in animal.habit():
                if a.act():
                    break
    
#동물 예시-JEHA는 JUMP,WALK,HELLO 의 우선순위로 행동
class JEHA(Animal):
    def habit():
        return [EXAMPLE_JUMPING(10),EXAMPLE_WALK(),EXAMPLE_HELLO()]