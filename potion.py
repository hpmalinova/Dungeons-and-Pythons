from treasure import Treasure


class Potion(Treasure):
    potion_types = ['mana', 'health']

    def __init__(self, potion_type, points):
        self.validate_potion_type(potion_type)
        self.potion_type = potion_type

        assert points >= 0, 'Potion should have positive points'
        self.points = points

    @classmethod
    def from_list(cls, arguments):
        assert len(arguments) == 2, 'Invalid number of arguments'
        return cls(arguments[0], int(arguments[1]))

    def __str__(self):
        return f'{type(self).__name__} gives {self.points} {self.potion_type}.'

    def __repr__(self):
        return f'{type(self).__name__} gives {self.points} {self.potion_type}.'

    def __eq__(self, other):
        return self.potion_type == other.potion_type and self.points == other.points

    @staticmethod
    def validate_potion_type(potion_type):
        assert potion_type in Potion.potion_types, 'Invalid potion type'
