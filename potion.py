from treasure import Treasure


class Potion(Treasure):
    potion_types = ['mana', 'health']

    def __init__(self, potion_type, points):
        self.validate_potion_type(potion_type)

        self.potion_type = potion_type
        self.points = points

    def equip_to(self, hero):
        hero.drink_potion(self)

    @staticmethod
    def validate_potion_type(potion_type):
        assert potion_type in Potion.potion_types, 'Invalid potion type'
