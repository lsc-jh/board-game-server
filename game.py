import random
from typing import Dict, List
from models import Pos, PlayerModel, EnemyModel, TreasureModel, WallModel, EmptyModel, TileModel

class Game:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.players: Dict[str, PlayerModel] = {}
        self.enemies: Dict[str, EnemyModel] = {}
        self.map: List[List[TileModel]] = [[EmptyModel(Pos(x, y)) for x in range(width)] for y in range(height)]
        self.walls: List[WallModel] = []
        self.treasure: TreasureModel | None = None
        self.exit = Pos(width - 2, height - 2)

        self._generate_walls()
        self._place_treasure()
        self._spawn_enemies(5)

        for wall in self.walls:
            self.map[wall.pos.y][wall.pos.x] = wall

    def _generate_walls(self):
        for x in range(self.width):
            self.walls.append(WallModel(Pos(x, 0)))
            self.walls.append(WallModel(Pos(x, self.height - 1)))
        for y in range(self.height):
            self.walls.append(WallModel(Pos(0, y)))
            self.walls.append(WallModel(Pos(self.width - 1, y)))
        for _ in range((self.width * self.height) // 10):
            self.walls.append(WallModel(Pos(random.randint(1, self.width - 2), random.randint(1, self.height - 2))))

    def _place_treasure(self):
        self.treasure = TreasureModel(Pos(random.randint(1, self.width - 2), random.randint(1, self.height - 2)))

    def _spawn_enemies(self, count):
        for _ in range(count):
            pos = Pos(random.randint(1, self.width - 2), random.randint(1, self.height - 2))
            enemy = EnemyModel(pos)
            self.enemies[enemy.id] = enemy

    def add_player(self) -> str:
        player = PlayerModel(Pos(1, 1))
        self.players[player.id] = player
        return player.id

    def remove_player(self, player_id):
        self.players.pop(player_id, None)

    def move_player(self, player_id, direction):
        if player_id not in self.players:
            return
        dx, dy = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}.get(direction, (0, 0))
        self.players[player_id].move(dx, dy, self.map)

        if self.treasure and not self.treasure.collected:
            if (self.players[player_id].pos.x == self.treasure.pos.x and
                self.players[player_id].pos.y == self.treasure.pos.y):
                self.treasure.collect(player_id)

    def move_enemies(self):
        for enemy in self.enemies.values():
            enemy.move_random(self.map)

    def get_init(self):
        return {
            "type": "init",
            "width": self.width,
            "height": self.height,
            "walls": [w.pos.to_dict() for w in self.walls],
            "exit": self.exit.to_dict(),
        }

    def get_state(self, current_player_id):
        return {
            "type": "state",
            "you": current_player_id,
            "players": {pid: p.pos.to_dict() for pid, p in self.players.items()},
            "enemies": {eid: e.pos.to_dict() for eid, e in self.enemies.items()},
            "treasure": {
                "x": self.treasure.pos.x if self.treasure else None,
                "y": self.treasure.pos.y if self.treasure else None,
                "collected": self.treasure.collected if self.treasure else None,
                "collected_by": self.treasure.collected_by if self.treasure else None,
            }
        }
