import pygame


class Agent:
    def __init__(self, id1: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self.id = id1
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.orderList = []
        self.lastDest = 0
        self.image = pygame.image.load('../images/Pokeball.png')


