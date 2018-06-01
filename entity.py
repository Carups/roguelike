import math
import random
from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, render_order=RenderOrder.CORPSE, blocks=False,
                 fighter=None, ai=None, item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.render_order = render_order
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        path = game_map.compute_path(self.x, self.y, target_x, target_y)

        dx = path[0][0] - self.x
        dy = path[0][1] - self.y
        if dx != 0 and dy != 0:
            if random.randint(0, 1) == 1:
                dx = 0
            else:
                dy = 0

        if game_map.walkable[self.x + dx, self.y + dy] and not get_blocking_entities_at_location(entities, self.x + dx,
                                                                                               self.y + dy):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return abs(dx) + abs(dy)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None