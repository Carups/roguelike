import random
from config import Config
from game_messages import Message
class Item:
    """
    Primitive item. You can pick up and drop out or use this objects
    """
    def __init__(self):
        self.short = 'i'

    def pick_up(self, target, holder):
        pass

    def use(self, target):
        pass


class HealPotion(Item):
    """
    Item that you can use and get extra health from 5 to 15
    """
    def __init__(self):
        self.short = '!'
        self.heal = 5 * random.randint(1, 3)

    def pick_up(self, target, holder):
        return target.inventory.add_item(holder)

    def use(self, target):
        if target.fighter is not None:
            return target.fighter.recover(self.heal)
        else:
            return {"message": "Your potion wasted"}


class Sword(Item):
    '''
    Regular sword that increased attack
    '''
    def __init__(self):
        self.short = "s"
        self.attack = random.randint(1, 10)

    def pick_up(self, target, holder):
        equiped = False
        for each in target.inventory.items:
            if each.item is not None:
                if each.item.__class__ == Sword:
                        equiped = True
        if equiped:
            return [{
                'pick_up': None,
                'message': Message('You already have a sword!', Config.colors.get('blue'))
            }]
        result = target.fighter.power_up(self.attack)
        result.extend(target.inventory.add_item(holder))
        return result


    def use(self, target):
        return [{
                'item_droped': self,
                'message': Message('You drop the sword!', Config.colors.get('blue'))
            }]


class Armor(Item):
    '''
    Regular armor that increased armor
    '''
    def __init__(self):
        self.short = 'a'
        self.armor = random.randint(1, 10)
    def pick_up(self, target, holder):
        equiped = False
        for each in target.inventory.items:
            if each.item is not None:
                if each.item.__class__ == Armor:
                    equiped = True
        if equiped:
            return [{
                'pick_up': None,
                'message': Message('You already have a armor!', Config.colors.get('blue'))
                }]
        result = target.fighter.armor_up(self.armor)
        result.extend(target.inventory.add_item(holder))
        return result

    def use(self, target):
        return [{
                'item_droped': self,
                'message': Message('You drop the armor!', Config.colors.get('blue'))
               }]

