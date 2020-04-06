# hero.py

from .human import Human


class Hero(Human):
    # Constructor

    def __init__(self, name, title, health, mana, mana_regeneration_rate):
        super().__init__(health, mana)

        self.validate_input_hero(name, title, mana_regeneration_rate)

        self.name = name
        self.title = title
        self.mana_regeneration_rate = mana_regeneration_rate

    def get_spell_cast_range(self):
        if not self.spell:
            return -1
        return getattr(self.spell, 'cast_range')

    # Public

    def known_as(self):
        return f'{self.name} the {self.title}'

    def take_mana(self, mana_points):
        if self.mana + mana_points > self.max_mana:
            self.mana = self.max_mana
        else:
            self.mana += mana_points

    def regenerate_mana(self):
        self.take_mana(self.mana_regeneration_rate)

    def attack(self, by=None):
        if not by:
            return self.get_strongest_mean()

        if by == 'weapon':
            return self.__attack_by_weapon()
        elif by == 'magic':
            return self.__attack_by_magic()

        else:
            raise ValueError('Unrecognized means of attack.')

    def __attack_by_weapon(self):
        if not self.weapon:
            return None
        else:
            return self.weapon

    def __attack_by_magic(self):
        if not self.spell or not self.can_cast():
            return None

        self.mana -= getattr(self.spell, 'mana_cost')
        return self.spell

    # Static

    @staticmethod
    def validate_input_hero(name, title, mana_regeneration_rate):
        if type(name) is not str:
            raise TypeError('Name must be of "str" type.')
        elif type(title) is not str:
            raise TypeError('Title must be of "str" type.')
        elif type(mana_regeneration_rate) is not int:
            raise TypeError('Mana regeneration rate must be of "int" type.')
        elif mana_regeneration_rate < 0:
            raise ValueError('Mana regeneration rate cannot be negative.')
