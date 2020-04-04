from treasure import Treasure


class Armor(Treasure):
    def __init__(self, name, armor_points):
        self.name = name
        assert armor_points >= 0, 'Ivalid armor points'
        self.armor_points = armor_points

    @classmethod
    def from_list(cls, arguments):
        assert len(arguments) == 2, 'Invalid number of arguments'
        return cls(arguments[0], int(arguments[1]))

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.armor_points == other.armor_points

    def __lt__(self, other):
        return self.armor_points < other.armor_points
