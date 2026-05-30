from base import Behaves, Entity, World
from geo import Vector


# 예시 코드
# 예시1-JUMP는 speed가 10 이상, 배고픔이 10 이상이여야 할 수 있고, 실행시 pos를 +val,+val한다
class EXAMPLE_JUMPING(Behaves):
    def __init__(self, val):
        self.val = val

    def act(self, entity, world):
        if entity.speed < 10 or entity.hunger < 10:
            return False
        entity.pos += Vector(self.val, self.val)
        return True


# 예시2-WALK는 배고픔이 4 이상이면 할 수 있다
class EXAMPLE_WALK(Behaves):
    def act(self, entity, world):
        if entity.hunger < 4:
            return False
        entity.pos += Vector(4, 4)
        return True


# 예시3-HELLO는 언제나 할 수 있다
class EXAMPLE_HELLO(Behaves):
    def act(self, entity, world):
        print("hello!!!!!!!!!!!!!")
        return True
