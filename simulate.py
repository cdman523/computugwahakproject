# 시각화 코드
from pygame import *
from base import World


class Simulator:
    def __init__(self):
        self.world = World()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            pass
