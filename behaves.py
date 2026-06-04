from base import Behaves, Animal, Entity, World, Carcass
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
class LION_GUARD_CARCASS(Behaves):
    """
    사냥한 시체 주변에 머물러 하이에나 접근을 막는다.
    - 감지 범위 내 Carcass가 있으면 그 쪽으로 이동하며 자리를 지킨다.
    - 시체가 없으면 False → 다음 행동으로 넘어감.
    """
    GUARD_RANGE = 30

    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World) -> bool:
        carcass = world.findnearesttarget(
            self.actor, (Carcass,), findrange=self.actor.sight
        )
        if carcass is None:
            return False

        if self.actor.pos.distance_to(carcass.pos) > self.GUARD_RANGE:
            self.actor.move(self.actor.speed, carcass.pos)
        return True
class LION_REST(Behaves):
    """
    배가 부른 사자는 초식동물이 곁을 지나가도 사냥하지 않고 휴식한다.
    hunger가 MAX_HUNGER의 80% 이상이면 True를 반환하여 뒤 행동을 막는다.
    """
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World) -> bool:
        if self.actor.hunger < self.actor.MAX_HUNGER * 0.8:
            return False
        return True  # 배부름 → 휴식, 사냥 차단
class LION_HUNT_PACK(Behaves):
    """
    Buffalo는 체력·방어력이 높아 무리 사냥이 필요하다.
    - 감지 범위 내 Buffalo를 발견하면 근처 사자들을 소집해 함께 이동한다.
    - 자신 포함 MIN_LIONS 마리 이상 모이면 공격까지 수행한다.
    - Buffalo가 없으면 False → ATTACK_TARGET으로 넘어감.
    """
    MIN_LIONS = 2

    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World) -> bool:
        from animals import Buffalo
        target = world.findnearesttarget(
            self.actor, (Buffalo,), findrange=self.actor.sight
        )
        if target is None:
            return False

        # 근처 사자들을 Buffalo 방향으로 소집
        nearby_lions = [
            e for e in world.entities
            if e.__class__.__name__ == "Lion"
            and e is not self.actor
            and self.actor.pos.distance_to(e.pos) <= self.actor.sight
        ]
        for lion in nearby_lions:
            lion.move(lion.speed, target.pos)

        self.actor.move(self.actor.speed, target.pos)

        # 충분히 모였으면 공격
        if len(nearby_lions) + 1 >= self.MIN_LIONS:
            if self.actor.pos.distance_to(target.pos) <= 15:
                damage = max(1, self.actor.attack - target.defense)
                target.hp -= damage
                if target.hp <= 0:
                    target.dead()

        return True
class ZEBRA_ALERT(Behaves):
    """
    시력이 좋은 얼룩말이 포식자(Lion, Hyena)를 먼저 발견하면
    감지 범위 내 Gazelle에게도 도주 신호를 전달한다.
    - 포식자가 없으면 False.
    - 있으면 자신과 근처 Gazelle 모두 RUNAWAY 실행.
    """
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World) -> bool:
        from animals import Lion, Hyena, Gazelle
        predator = world.findnearesttarget(
            self.actor, (Lion, Hyena), findrange=self.actor.sight
        )
        if predator is None:
            return False

        # 근처 가젤에게 도주 신호 전파
        nearby_gazelles = world.findtarget(
            self.actor, (Gazelle,), findrange=self.actor.sight
        )
        for gazelle in nearby_gazelles:
            RUNAWAY(gazelle).act(world)

        RUNAWAY(self.actor).act(world)
        return True


class RUNAWAY(Behaves):
    """
    포식자로부터 도망치되, 코끼리 근처로 이동하여 생존율을 높인다.
    - 감지 범위 내 포식자가 없으면 False.
    - Elephant가 감지 범위 내에 있으면 코끼리 방향으로 이동.
    - 없으면 포식자 반대 방향으로 한 스텝 이동.
    """
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World) -> bool:
        from animals import Lion, Hyena, Elephant
        predator = world.findnearesttarget(
            self.actor, (Lion, Hyena), findrange=self.actor.sight
        )
        if predator is None:
            return False

        elephant = world.findnearesttarget(
            self.actor, (Elephant,), findrange=self.actor.sight
        )

        if elephant is not None:
            self.actor.move(self.actor.speed, elephant.pos)
        else:
            # 포식자 반대 방향으로 한 스텝 — move()가 방향+거리 계산하므로
            # 현재 pos에서 충분히 먼 반대 지점을 목표로 넘긴다
            away = self.actor.pos + (self.actor.pos - predator.pos).normalize() * 9999
            self.actor.move(self.actor.speed, away)

        return True

