# enemy.py

from human import Human

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
        weapon_damage = 0
        spell_damage = 0

        if self.weapon is not None:
            weapon_damage = getattr(self.weapon, 'damage')
        if self.spell is not None and self.mana >= getattr(self.spell, 'mana_cost'):
            spell_damage = getattr(self.spell, 'damage')

        max_damage = max(self.damage, weapon_damage, spell_damage)

        if max_damage == spell_damage:
            self.mana -= getattr(self.spell, 'mana_cost')
            return getattr(self.spell, 'damage')
        else:
            return max_damage

    # Static

    @staticmethod
    def validate_input_enemy(damage):
        if type(damage) is not int and type(damage) is not float:
            raise TypeError('Damage must be of "int" / "float" type.')
        elif damage < 0:
            raise Exception('Damage cannot be negative.')