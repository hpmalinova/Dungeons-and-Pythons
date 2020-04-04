from treasure import Treasure


class Weapon(Treasure):
    def __init__(self, name, damage):
        self.name = name
        assert damage >= 0, 'Damage of weapon can`t be a negative number'
        self.damage = damage

    @classmethod
    def from_list(cls, arguments):
        assert len(arguments) == 2, 'Invalid number of arguments'
        return cls(arguments[0], int(arguments[1]))

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.damage == other.damage

    def __lt__(self, other):
        return self.damage < other.damage
