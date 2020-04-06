from .treasure import Treasure


class Spell(Treasure):
    def __init__(self, name, damage, mana_cost, cast_range):
        self.name = name

        assert damage >= 0, 'Damage dealt can`t be a negative number.'
        self.damage = damage

        assert mana_cost >= 0, 'Mana cost can`t be a negative number.'
        self.mana_cost = mana_cost

        assert cast_range >= 0, 'Cast range can`t be a negative number.'
        self.cast_range = cast_range

    @classmethod
    def from_list(cls, arguments):
        assert len(arguments) == 4, 'Invalid number of arguments'
        return cls(arguments[0], int(arguments[1]), int(arguments[2]), int(arguments[3]))

    def __str__(self):
        return (f'{type(self).__name__}: {self.name} deals {self.damage} damage, '
                f'costs {self.mana_cost} and has range {self.cast_range}.')

    def __repr__(self):
        return (f'{type(self).__name__}: {self.name} deals {self.damage} damage, '
                f'costs {self.mana_cost} and has range {self.cast_range}.')

    def __eq__(self, other):
        return self.name == other.name and self.damage == other.damage and \
            self.mana_cost == other.mana_cost and self.cast_range == other.cast_range

    def __lt__(self, other):
        return self.damage < other.damage
