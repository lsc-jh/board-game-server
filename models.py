class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}


class Player:
    def __init__(self, player_id, pos: Pos):
        self.id = player_id
        self.pos = pos

    def move(self, dx, dy, width, height):
        self.pos.x = max(1, min(width - 2, self.pos.x + dx))
        self.pos.y = max(1, min(height - 2, self.pos.y + dy))


class Enemy:
    def __init__(self, pos: Pos):
        self.pos = pos

    def move_random(self, width, height):
        import random
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.pos.x = max(1, min(width - 2, self.pos.x + dx))
        self.pos.y = max(1, min(height - 2, self.pos.y + dy))