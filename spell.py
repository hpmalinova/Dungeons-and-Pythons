from treasure import Treasure


class Spell(Treasure):
    def __init__(self, name, damage, mana_cost, cast_range):
        self.name = name

        assert damage >= 0, 'Damage dealt can`t be a negative number.'
        self.damage = damage

        assert mana_cost >= 0, 'Mana cost can`t be a negative number.'
        self.mana_cost = mana_cost

        assert cast_range >= 0, 'Cast range can`t be a negative number.'
        self.cast_range = cast_range

    def __eq__(self, other):
        return self.name == other.name and self.damage == other.damage and \
            self.mana_cost == other.mana_cost and self.cast_range == other.cast_range

    def __lt__(self, other):
        return self.damage < other.damage

    def equip_to(self, human):
        human.learn(self)
