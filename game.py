import random
from models import Pos, Player, Enemy

class Game:
    def __init__(self, width=40, height=40):
        self.width = width
        self.height = height
        self.players = {}
        self.enemies = []
        self.walls = []
        self.treasure = None
        self.exit = Pos(width - 2, height - 2)

        self._generate_walls()
        self._place_treasure()
        self._spawn_enemies(5)

    def _generate_walls(self):
        for x in range(self.width):
            self.walls.append(Pos(x, 0))
            self.walls.append(Pos(x, self.height - 1))
        for y in range(self.height):
            self.walls.append(Pos(0, y))
            self.walls.append(Pos(self.width - 1, y))
        for _ in range((self.width * self.height) // 10):
            self.walls.append(Pos(random.randint(1, self.width - 2), random.randint(1, self.height - 2)))

    def _place_treasure(self):
        self.treasure = Pos(random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        self.treasure_collected = False

    def _spawn_enemies(self, count):
        for _ in range(count):
            pos = Pos(random.randint(1, self.width - 2), random.randint(1, self.height - 2))
            self.enemies.append(Enemy(pos))

    def add_player(self, player_id):
        self.players[player_id] = Player(player_id, Pos(1, 1))

    def remove_player(self, player_id):
        self.players.pop(player_id, None)

    def move_player(self, player_id, direction):
        if player_id not in self.players:
            return
        dx, dy = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}.get(direction, (0, 0))
        self.players[player_id].move(dx, dy, self.width, self.height)

        if (self.players[player_id].pos.x == self.treasure.x and
            self.players[player_id].pos.y == self.treasure.y):
            self.treasure_collected = True

    def get_init(self):
        return {
            "type": "init",
            "width": self.width,
            "height": self.height,
            "walls": [p.to_dict() for p in self.walls],
            "exit": self.exit.to_dict(),
        }

    def get_state(self, current_player_id):
        return {
            "type": "state",
            "you": current_player_id,
            "players": {pid: p.pos.to_dict() for pid, p in self.players.items()},
            "enemies": [e.pos.to_dict() for e in self.enemies],
            "treasure": {
                "x": self.treasure.x,
                "y": self.treasure.y,
                "collected": self.treasure_collected
            }
        }