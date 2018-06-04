from game_messages import Message
from config import Config

class Inventory:
    """
    Keep track on players inventory
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', Config.colors.get('yellow'))
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), Config.colors.get('blue'))
            })

            self.items.append(item)

        return results

    def drop_item(self, item):
        results = []

        if item in self.items:
            results.append({
                'item_droped': item,
                'message': Message('You pick up the {0}!'.format(item.name), Config.colors.get('blue'))
            })
        else:
            results.append({
                'item_droped': None,
                'message': Message('This item does not exist', Config.colors.get('yellow'))
            })

            self.items.remove(item)

        return results

    def remove(self, index):
        self.items.remove(self.items[index])
