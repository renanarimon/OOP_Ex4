import pygame


class Pokemon:
    def __init__(self, value: float, type: int, pos: tuple, id1: int):
        self.value = value
        self.type = type
        self.pos = pos
        self.posScale = pos
        self.id = id1
        self.took = False
        self.image_U = pygame.image.load('../images/bluePokemon.png')
        self.image_D = pygame.image.load('../images/Pikachu.png')

    def __str__(self):
        return self.pos
