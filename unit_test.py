import unittest
from map_utils import make_map, GameMap
from config import Config
from entity import Entity

class TestMake_map(unittest.TestCase):
    def test_map_is_connected(self):
        game_map = GameMap(Config.map_width, Config.map_height)
        player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True)
        entities = [player]
        make_map(game_map, Config.max_rooms, Config.room_min_size, Config.room_max_size, Config.map_width,
                 Config.map_height, player, entities, Config.max_monsters_per_room, Config.colors)
        was = []

        def dfs(x, y):
            if (x, y) in was:
                return
            was.append((x, y))
            dx = [-1, 0, 1, 0]
            dy = [0, 1, 0, -1]
            for j in range(4):
                tx = x + dx[j]
                ty = y + dy[j]
                if tx >= 0 and tx < Config.map_width and \
                     ty >= 0 and ty < Config.map_height and game_map.walkable[tx, ty]:
                        dfs(tx, ty)

        def check():
            for x in range(Config.map_width):
                for y in range(Config.map_height):
                    if game_map.walkable[x, y]:
                        self.assertTrue((x, y) in was, True)

        for i in range(Config.map_width):
            for j in range(Config.map_height):
                if game_map.walkable[i, j]:
                    dfs(i, j)
                    check()
                    return

if __name__ == '__main__':
    run = 0
    unittest.main()