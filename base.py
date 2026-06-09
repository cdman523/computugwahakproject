from abc import ABC, abstractmethod
import pygame
import random as r


class Entity(ABC):
    def __init__(self, pos: pygame.Vector2):
        self.pos = pos
        self.isdead=False

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
        self.entity_map[ett] = ett.pos
        if isinstance(ett,Animal):
            addlog(f'{ett.name}을(를) 소환했습니다.')

    def update(self):
        for entity in self.entities:
            if not entity.isdead:
                for a in entity.habit():
                    if a.act(self):
                        if isinstance(entity,Animal):
                            entity.hunger-=0.01
                            if entity.hunger<=0:
                                entity.hp-=0.05
                            elif entity.hunger>=entity.MAXHUNGER*0.9:
                                entity.hp+=0.1
                        break
        for gra in self.grass_map:
            for ss in gra:
                ss.grow(r.uniform(0.1,1.5))

    def remove(self, entity: "Entity"):
        del self.entity_map[entity]

    def findtarget(self, entity: "Entity", targetlist=None, findrange=float("inf")):
        return [
            an
            for an in self.entities
            if (targetlist is None or isinstance(an, targetlist))
            and (an.pos.distance_to(entity.pos)) <= findrange
            and an!=entity
        ]

    def findnearesttarget(self, entity:Entity, targetlist=None, findrange=float("inf"))->Entity|None:
        targets = self.findtarget(entity, targetlist, findrange)
        if len(targets) == 0:
            return None
        return min(targets, key=lambda aa: aa.pos.distance_to(entity.pos))
    
    def wheregrass(self,entity):
        return (int(entity.pos.x//75),int(entity.pos.y//75))


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
        self.isdead=False
        self.name = name
        self.maxhp=self.hp = hp
        self.attack = attack
        self.defense = defense
        self.hunger = hunger
        self.speed = speed
        self.sight = sight
        self.pos = pos
        self.world = world
        
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self,v):
        if self.isdead:
            return
        self._hp=v if v<=self.maxhp else self.maxhp
        if self.hp<=0:
            self.dead()

    @property
    def hunger(self):
        return self._hunger
    
    @hunger.setter
    def hunger(self,v):
        self._hunger=v if 0<=v<=self.MAXHUNGER else 0 if v<0 else self.MAXHUNGER



    def move(self, speed, goto: pygame.Vector2):
        if goto.x<20 or goto.x>1180 or goto.y<20 or goto.y>730:
            return self.move(speed,pygame.Vector2(max(min(1180,goto.x),20),max(min(730,goto.y),20)))
        self.pos = goto
        if speed > self.speed:
            self.hunger -= (speed-self.speed)/self.speed
        self.world.entity_map[self]=goto
        return f"{self.name}이 {goto.x},{goto.y}로 이동"

    def dead(self):
        if self.isdead:
            return
        self.isdead=True
        self.world.summon(Carcass, self.pos)
        self.world.remove(self)
        addlog(f'{self.name}이(가) 사망했습니다.')


class Carcass(Entity):
    def __init__(self, remain: float, pos: "pygame.Vector2", world):
        self.remain = remain
        self.pos = pos
        self.isdead=False

    @classmethod
    def info(cls):
        return (100,)

    def habit(self) -> list["Behaves"]:
        return [Rot(self)]

    def surface(self):
        sf = pygame.transform.scale(
            pygame.image.load("images/carcas.png"), (90, 90)
        )
        sf.set_alpha(int(self.remain * 255 / 100))
        return sf


class Rot(Behaves):
    ROT_VELOCITY = 0.05

    def __init__(self, carcass: Carcass):
        self.carcass = carcass

    def act(self, world: World) -> bool:
        if self.carcass.remain <= 0:
            self.carcass.isdead=True
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

class Nuclear(Entity):
    def __init__(self,pos,world):
        self.isdead=False
        super().__init__(pygame.Vector2(pos.x,-100))
        self.targetpos=pos
        self.world=world
    def fall(self,v):
        self.pos.y+=v
        self.world.entity_map[self].y+=v
    @classmethod
    def info(cls):
        return ()
    def habit(self):
        return [BombFall(self)]
    def surface(self):
        return pygame.transform.scale(pygame.image.load('images/suwoobomb.png'),(200,200))
    
class BombFall(Behaves):
    def __init__(self,bomb):
        self.bomb=bomb
    def act(self,world):
        self.bomb.fall(5)
        if self.bomb.pos.y>=self.bomb.targetpos.y:
            world.summon(Explosion,self.bomb.pos)
            self.bomb.isdead=True
            world.remove(self.bomb)
        return True

class Explosion(Entity):
    def __init__(self,pos,world):
        super().__init__(pos)
        self.world=world
        self.radius=10
        self.mradius=1500
        self.alpha=255
    @classmethod
    def info(cls):
        return ()
    def habit(self):
        return [NuclearBomber(self)]
    def surface(self):
        size=int(self.radius*0.5)
        sf=pygame.transform.scale(pygame.image.load('images/suwooattack.png'),(size,size))
        sf.set_alpha(self.alpha)
        return sf

class NuclearBomber(Behaves):
    def __init__(self,explosion):
        self.explosion=explosion
    def act(self,world):
        self.explosion.radius+=8
        self.explosion.alpha-=1
        for entity in world.entities:
            if not isinstance(entity,Animal) or entity.isdead: continue
            if entity.pos.distance_to(self.explosion.pos)<=self.explosion.radius:
                entity.hp=0
        if self.explosion.radius >= self.explosion.mradius or self.explosion.alpha <= 0:
            self.explosion.isdead = True
            world.remove(self.explosion)