from base import Behaves, Animal, Entity, World
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
            if isinstance(entity, Buffalo) and entity is not self.actor:
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


class ATTACK_TARGET(Behaves):
    def __init__(self, predator: Animal, target_types: list):
        self.predator = predator
        self.target_types = tuple(target_types)

    def act(self, world: World):
        # 기획 조건: 배가 부르면 사냥하지 않고 쉼
        if self.predator.hunger > self.predator.max_hunger * 0.8:
            return False
            
        target = world.findnearesttarget(self.predator, self.target_types, findrange=self.predator.sight)
        if target and isinstance(target, Animal):
            # 코끼리가 근처에 있으면 접근 금지 조건 우회
            from animals import Elephant
            if world.findnearesttarget(self.predator, Elephant, findrange=80):
                return False

            if self.predator.pos.distance_to(target.pos) > 15:
                # 사냥할 때는 원래 속도보다 빠르게 뜀
                self.predator.move(self.predator.speed * 1.3, target.pos)
            else:
                # 공격 연산
                damage = max(1, self.predator.attack - target.defense)
                target.hp -= damage
            return True
        return False