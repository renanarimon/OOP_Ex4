class Pokemon:
    def __init__(self, value: float, type: int, pos: tuple, id1: int):
        self.value = value
        self.type = type
        self.pos = pos
        self.posScale = pos
        self.id = id1
        self.took = False

    def __str__(self):
        return self.pos
