# enemy.py

from .human import Human
from .weapon import Weapon


class Enemy(Human):
    # Constructor

    def __init__(self, health, mana, damage):
        super().__init__(health, mana)

        self.validate_input_enemy(damage)

        self.damage = damage

    def take_mana(self):
        print('Enemies cannot regenerate mana.')
        return False

    def attack(self):
        strongest_weapon = self.get_strongest_mean()

        if not strongest_weapon or self.damage > getattr(strongest_weapon, 'damage'):
            return Weapon('Fists', self.damage)

        return strongest_weapon

    # Static

    @staticmethod
    def validate_input_enemy(damage):
        if type(damage) is not int and type(damage) is not float:
            raise TypeError('Damage must be of "int" / "float" type.')
        elif damage <= 0:
            raise ValueError('Damage should be positive.')
