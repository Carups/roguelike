import random
class Item:
    def __init__(self):
        pass

    def use(self, target):
        pass

class HealPotion(Item):
    def __init__(self):

        self.heal = 5 * random.randint(1, 3)

    def use(self, target):
        if target.fight:
            return target.fight.heal(self.heal)
        else:
            return {"message": "Your potion wasted"}
