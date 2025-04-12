import random
import uuid
from typing import List

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}

class TileModel:
    def __init__(self, walkable: bool, pos: Pos):
        self.walkable = walkable
        self.pos = pos

    def to_dict(self):
        return {
            "walkable": self.walkable,
            "pos": self.pos.to_dict()
        }

class EmptyModel(TileModel):
    def __init__(self, pos: Pos):
        super().__init__(True, pos)


class WallModel(TileModel):
    def __init__(self, pos: Pos):
        super().__init__(False, pos)


class EntityModel(TileModel):
    def __init__(self, walkable: bool, pos: Pos):
        self.id = str(uuid.uuid4())
        super().__init__(walkable, pos)

    def _move(self, dx, dy, map: List[List[TileModel]]):
        new_x = self.pos.x + dx
        new_y = self.pos.y + dy

        if map[new_y][new_x].walkable:
            self.pos.x = new_x
            self.pos.y = new_y


class PlayerModel(EntityModel):
    def __init__(self, pos: Pos):
        super().__init__(True, pos)
        self.items = []

    def move(self, dx, dy, map: List[List[TileModel]]):
        self._move(dx, dy, map)


class TreasureModel(TileModel):
    def __init__(self, pos: Pos):
        self.collected = False
        self.collected_by = None
        super().__init__(True, pos)

    def collect(self, player_id):
        self.collected = True
        self.collected_by = player_id


class EnemyModel(EntityModel):
    def __init__(self, pos: Pos):
        super().__init__(False, pos)

    def move_random(self, map: List[List[TileModel]]):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self._move(dx, dy, map)
