from base import Behaves, Animal, Entity, World, Carcass,addlog,Nuclear,Explosion,normalize
from animals import *
from pygame import Vector2
import random as r
# 예시 코드
# 예시1-JUMP는 speed가 10 이상, 배고픔이 10 이상이여야 할 수 있고, 실행시 pos를 +val,+val한다

class EXAMPLE_JUMPING(Behaves):
    def __init__(self, jumper: Animal, val):
        self.val = val
        self.jumper = jumper

    def act(self, world: World):
        if self.jumper.speed < 10 or self.jumper.hunger < 10:
            return False
        self.jumper.move(20,self.jumper.pos+Vector2(self.val,self.val))
        return True


# 예시2-WALK는 배고픔이 4 이상이면 할 수 있다
class EXAMPLE_WALK(Behaves):
    def __init__(self, walker: Animal):
        self.walker = walker

    def act(self, world: World):
        if self.walker.hunger < 4:
            return False
        self.walker.move(15,self.walker.pos+Vector2(4,4))
        return True


# 예시3-HELLO는 언제나 할 수 있다
class EXAMPLE_HELLO(Behaves):
    def __init__(self, hellower):
        self.hellower = hellower

    def act(self, world: World):
        return True


class DONOTHING(Behaves):
    def __init__(self,er):
        self.er=er
    def act(self,world:World):
        return True
    
class BUFFALO_MOVE_TO_BUFFALO(Behaves):
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World):
        target = world.findnearesttarget(
            entity=self.actor, 
            targetlist=type(self.actor), 
            findrange=self.actor.sight
        )

        if target is None:
            return False
        self.actor.state=['donot']
        direction = target.pos - self.actor.pos
        if direction.length() > 40:
            direction = normalize(direction)
            speed = self.actor.speed
            goto = self.actor.pos + direction * speed
            self.actor.move(speed, goto)            
            return True
        return False
    
class GAZELLE_MOVE_TO_GAZELLE(Behaves):
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World):
        target = world.findnearesttarget(
            entity=self.actor, 
            targetlist=type(self.actor), 
            findrange=self.actor.sight
        )
        
        if target is None:
            return False
        self.actor.state=['donot']      
        direction = target.pos - self.actor.pos
        if direction.length() > 40:
            direction=normalize(direction)
            speed = self.actor.speed
            goto = self.actor.pos + direction * speed
            self.actor.move(speed, goto)            
            return True
        return False

class CHARGE_RUSH(Behaves):
    def __init__(self, actor: Animal):
        self.actor = actor
        self.detect_radius = 60.0  
        self.damage_radius = 30.0   
        self.rush_speed_mult = 2  
        self.collision_damage = 0.2

    def act(self, world: World):
        predator_names = ["Lion", "Hyena"] 
        nearby_animals = world.findtarget(self.actor, Animal, self.detect_radius)
        predators = [an for an in nearby_animals if an.__class__.__name__ in predator_names]
        
        if not predators:
            return False 

        escape_dir = Vector2(0, 0)
        for p in predators:
            escape_dir += (self.actor.pos - p.pos)
        
        escape_dir=normalize(escape_dir)

        rush_speed = self.actor.speed * self.rush_speed_mult
        goto = self.actor.pos + (escape_dir * rush_speed )
        self.actor.state=['rush']
        for _ in range(6):
            self.actor.move(rush_speed, goto)

            hit_targets = world.findtarget(self.actor, Animal, self.damage_radius)
            for target in hit_targets:
                target.hp -= self.collision_damage
                target.attacker=self.actor
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

            self.predator.state=['hunting',target]
            if self.predator.pos.distance_to(target.pos) > 50:
                self.predator.move(self.predator.speed * 1.3, self.predator.pos+normalize(target.pos+normalize(Vector2(0,0))*30-self.predator.pos)*self.predator.speed*1.3)
            else:
                damage = max(1, self.predator.attack - target.defense)
                target.hp -= damage
                target.attacker=self.predator
            return True
        return False

class EAT_GRASS(Behaves):
    def __init__(self,eater,eat):
        self.eater=eater
        self.eat=eat
    def act(self,world:World):
        grassx,grassy=world.wheregrass(self.eater)
        if world.grass_map[grassy][grassx].remain<=self.eat+0.1 or self.eater.hunger>self.eater.MAXHUNGER*0.9:
            return False
        self.eater.state=['eatgrass']
        self.eater.hunger+=0.2
        world.grass_map[grassy][grassx].remain-=self.eat
        return True

class EAT_CARCASS(Behaves):
    def __init__(self, actor: Animal):
        self.actor=actor

    def act(self, world: World):
        if self.actor.hunger > self.actor.MAXHUNGER * 0.9:
            return False
        
        target = world. findnearesttarget(self.actor, Carcass, findrange=self.actor.sight)
        if target:
        #사자는 신선한 많이 남은 시체만 먹음. 하이에나는 남은 양 무관.
            from animals import Lion
            if isinstance(self.actor, Lion) and target.remain < 70:
                return False
            self.actor.state=['eatcarcass']
        #시체 근처로 이동 후 섭취
            if self.actor.pos.distance_to(target.pos) > 30:
                self.actor.move(self.actor.speed,self.actor.pos+normalize(target.pos-self.actor.pos)*self.actor.speed)
            else:
                target.remain-=0.5
                self.actor.hunger+=0.5
                self.actor.hp+=0.1
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
        from animals import Hyena
        hyena=world.findnearesttarget(self.actor,(Hyena,),findrange=self.actor.sight)
        if hyena is None:
            return False
        carcass = world.findnearesttarget(
            self.actor, (Carcass,), findrange=self.actor.sight
        )
        if carcass is None:
            return False
        self.actor.state=['donot']
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
        if self.actor.hunger < self.actor.MAXHUNGER * 0.8:
            return False
        self.actor.state=['donot']
        self.actor.move(self.actor.speed*0.1,self.actor.pos+normalize(Vector2(0,0)))
        return True  # 배부름 → 휴식, 사냥 차단
    
class LION_HUNT_PACK(Behaves):
    """
    Buffalo는 체력·방어력이 높아 무리 사냥이 필요하다.
    - 감지 범위 내 Buffalo를 발견하면 근처 사자들을 소집해 함께 이동한다.
    - 자신 포함 MIN_LIONS 마리 이상 모이면 공격까지 수행한다.
    - Buffalo가 없으면 False → ATTACK_TARGET으로 넘어감.
    """
    MIN_LIONS = 6

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
        if len(nearby_lions)+1>=self.MIN_LIONS-1:
            for lion in nearby_lions:
                lion.move(lion.speed, lion.pos+normalize(target.pos-lion.pos)*lion.speed)
            if target.pos.distance_to(self.actor.pos)>30:
                self.actor.move(self.actor.speed, self.actor.pos+normalize(target.pos-self.actor.pos)*self.actor.speed)

            # 충분히 모였으면 공격
            if len(nearby_lions) + 1 >= self.MIN_LIONS:
                self.actor.state=['hunting',target]
                if self.actor.pos.distance_to(target.pos) <= 30:
                    damage = max(1, self.actor.attack - target.defense)
                    target.hp -= damage
                    target.attacker=self.actor
                    return True
        return False
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
            if elephant.pos.distance_to(self.actor.pos)<40: return False
            self.actor.move(self.actor.speed*1.3, self.actor.pos+normalize(elephant.pos-self.actor.pos)*self.actor.speed*1.3)
        else:
            # 포식자 반대 방향으로 한 스텝 — move()가 방향+거리 계산하므로
            # 현재 pos에서 충분히 먼 반대 지점을 목표로 넘긴다
            away = self.actor.pos + normalize(self.actor.pos - predator.pos) * self.actor.speed * 1.2
            self.actor.move(self.actor.speed*1.2, away)

        return True


    # 평상시 목적지 없이 배회 (단, 코끼리 주변에는 접근 불가)
    #자연스러운 랜덤 워크 구현 AI 도움받음
class WANDER(Behaves):
    def __init__(self, actor: Animal):
        self.actor = actor

    def act(self, world: World):
        self.actor.state=['donot']
        # 처음 방향 초기화
        if self.actor.dir.length_squared() == 0:
            self.actor.dir = Vector2(1, 0).rotate(
                r.uniform(0, 360)
            )

        # 3% 확률로 잠깐 멈춤
        if r.random() < 0.03:
            return True

        # 현재 방향 기준으로 조금만 흔들기
        angle = self.actor.dir.as_polar()[1]
        delta = r.gauss(0, 10)

        new_dir = Vector2(1, 0).rotate(
            angle + delta
        )

        # 기존 방향에 높은 가중치
        self.actor.dir = (
            self.actor.dir * 0.6 +
            new_dir * 0.4
        )

        # 정규화
        if self.actor.dir.length_squared() > 0:
            self.actor.dir = self.actor.dir.normalize()

        # 이동 목표
        target = (
            self.actor.pos
            + self.actor.dir * self.actor.speed
        )

        # 벽 회피
        margin = 50

        if target.x < margin:
            self.actor.dir.x = abs(self.actor.dir.x)

        elif target.x > 1200 - margin:
            self.actor.dir.x = -abs(self.actor.dir.x)

        if target.y < margin:
            self.actor.dir.y = abs(self.actor.dir.y)

        elif target.y > 750 - margin:
            self.actor.dir.y = -abs(self.actor.dir.y)

        # 아주 가끔 크게 방향 변경
        if r.random() < 0.03:
            self.actor.dir.rotate_ip(
                r.uniform(-120, 120)
            )

        self.actor.move(
            self.actor.speed,
            self.actor.pos + self.actor.dir * self.actor.speed
        )

        return True

class ATTACK_LION_WHEN_MANY(Behaves):
    def __init__(self,actor: Animal):
        self.actor=actor
    
    def act(self,world: World):
        from animals import Hyena, Lion
        lion_target = world.findnearesttarget(self.actor,Lion,findrange=self.actor.sight)
        if not lion_target or lion_target.isdead:
            return False
        nearby_hyena = world.findtarget(self.actor,Hyena,findrange=self.actor.sight)
        if len(nearby_hyena)+1>=6:
            self.actor.state=['hunting',lion_target]
            if self.actor.pos.distance_to(lion_target.pos)>30:
                self.actor.move(self.actor.speed*1.3, self.actor.pos+normalize(lion_target.pos-self.actor.pos)*self.actor.speed)
            else:
                damage = max(1, self.actor.attack - lion_target.defense)
                lion_target.hp -= damage
                lion_target.attacker=self.actor
            return True
            
        return False


