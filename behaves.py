from base import Behaves, Animal, Entity, World, Carcass
from animals import *
from pygame import Vector2


# 예시 코드
# 예시1-JUMP는 speed가 10 이상, 배고픔이 10 이상이여야 할 수 있고, 실행시 pos를 +val,+val한다

class EXAMPLE_JUMPING(Behaves):
    def __init__(self, jumper: Animal, val):
        self.val = val
        self.jumper = jumper

    def act(self, world: World):
        if self.jumper.speed < 10 or self.jumper.hunger < 10:
            return False
        self.jumper.pos += Vector2(self.val, self.val)
        return True


# 예시2-WALK는 배고픔이 4 이상이면 할 수 있다
class EXAMPLE_WALK(Behaves):
    def __init__(self, walker: Animal):
        self.walker = walker

    def act(self, world: World):
        if self.walker.hunger < 4:
            return False
        self.walker.pos += Vector2(4, 4)
        return True


# 예시3-HELLO는 언제나 할 수 있다
class EXAMPLE_HELLO(Behaves):
    def __init__(self, hellower):
        self.hellower = hellower

    def act(self, world: World):
        print("hello!!!!!!!!!!!!!")
        return True


class BUFFALO_MOVE_TO_BUFFALO(Behaves):
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World):
        target = None
        min_dist = float("inf")
        for entity in getattr(world, "entities", []):
            if entity.__class__.__name__ == "Buffalo" and entity is not self.actor:
                dist = self.actor.pos.distance_to(entity.pos)
                if dist < min_dist:
                    min_dist = dist
                    target = entity
        if target is None:
            return False
        direction = target.pos - self.actor.pos
        if direction.length() > 0:
            direction = direction.normalize()
            speed = getattr(self.actor, "speed", 2)
            self.actor.pos += direction * speed
        return True

class ATTACK_TARGET(Behaves):
    def __init__(self, predator: Animal, target_types: list):
        self.predator = predator
        self.target_types = tuple(target_types)

    def act(self, world: World):
        if self.predator.hunger > self.predator.MAXHUNGER * 0.8:
            return False
            
        target = world.findnearesttarget(self.predator, self.target_types, findrange=self.predator.sight)
        if target and isinstance(target, Animal):
            from animals import Elephant
            if world.findnearesttarget(self.predator, Elephant, findrange=80):
                return False

            if self.predator.pos.distance_to(target.pos) > 15:
                self.predator.move(self.predator.speed * 1.3, target.pos)
            else:
                damage = max(1, self.predator.attack - target.defense)
                target.hp -= damage
            return True
        return False

class EAT_GRASS(Behaves):
    def __init__(self,eater):
        self.eater=eater
    def act(self,world:World):
        grassx,grassy=world.wheregrass(self.eater)
        if world.grass_map[grassy][grassx]<=10 or self.eater.hunger>35:
            return False
        self.eater.hunger+=1
        world.grass_map[grassy][grassx]-=5
        return True

class EAT_CARCASS(Behaves):
    def __init__(self, actor: Animal):
        self.actor=actor

    def act(self, world: World):
        if self.actor.hunger > self.actor.MAXHUNGER * 0.7:
            return False
        
        target = world. findnearesttarget(self.actor, Carcass, findrange=self.actor.sight)
        if target:
            from animals import Lion
#사자는 신선한 많이 남은 시체만 먹음. 하이에나는 남은 양 무관.
            if isinstance(self.actor, Lion) and target.remain < 70:
                return False
        #시체 근처로 이동 후 섭취
            if self.actor.pos.distance_to(target.pos) > 10:
                self.actor.move(self.actor.speed,target.pos)
            else:
                target.remain-=5
                self.actor.hunger=min(self.actor.MAXHUNGER, self.actor.hunger + 10)
            return True
        return False
