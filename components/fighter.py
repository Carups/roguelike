from game_messages import Message


class Fighter:
    """
    Realization of interface for combat
    """
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name))})

        return results

    def recover(self, heal):
        results = []
        max_heal = self.max_hp - self.hp
        self.hp = min(self.hp + heal, self.max_hp)
        results.append({'message': Message('{0} healed by {1}'.format(self.owner.name.capitalize(), max_heal))})
        return results

    def power_up(self, power):
        results = []
        self.power += power
        results.append({'message': Message('{0} power increased by {1}'.format(self.owner.name.capitalize(), power))})
        return results

    def armor_up(self, armor):
        results = []
        self.defense += armor
        results.append({'message': Message('{0} defense increased by {1}'.format(self.owner.name.capitalize(), armor))})
        return results