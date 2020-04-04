# human.py

from weapon import Weapon
from spell import Spell
from armor import Armor
from potion import Potion


class Human:
    # Constructor

    def __init__(self, health, mana):
        self.validate_input_human(health, mana)

        self.max_health = health
        self.max_mana = mana

        self.health = health
        self.mana = mana

        self.weapon = None
        self.spell = None
        self.armor = None

    # Public

    def get_health(self):
        return self.health

    def get_mana(self):
        return self.mana

    def is_alive(self):
        return self.health != 0

    def can_cast(self):
        if self.spell:
            return self.mana >= getattr(self.spell, 'mana_cost')
        else:
            return False

    def take_healing(self, healing_points):
        if self.health == 0:
            return False
        elif healing_points + self.health > self.max_health:
            self.health = self.max_health
        else:
            self.health += healing_points

    def take_damage(self, damage):
        if type(damage) is not float and type(damage) is not int:
            raise TypeError('Damage must be of "int" / "float" type.')

        armor_points = 0

        if self.armor:
            armor_points = getattr(self.armor, 'armor_points')

        if damage > armor_points:
            damage -= armor_points

            self.health = (self.health - damage) if damage < self.health else 0

    # Equip

    def equip(self, item):
        equipable_items = {Weapon: 'weapon', Armor: 'armor', Spell: 'spell'}
        drinkable_items = [Potion]

        my_type = type(item)

        if my_type in equipable_items.keys():
            self.equip_item(item)
        elif my_type in drinkable_items: # Тук беше if и винаги влизаше в тайперър-а
            self.drink_potion(item)
        else:
            raise TypeError('Invalid item type.')

    def equip_item(self, item):
        items_map = {Weapon: 'weapon', Armor: 'armor', Spell: 'spell'}

        my_type = type(item)
        attribute_to_change = items_map[my_type]

        if my_type in items_map.keys():
            equipped_item = getattr(self, attribute_to_change)
            if equipped_item:
                if equipped_item < item:
                    setattr(self, attribute_to_change)
            else:
                setattr(self, attribute_to_change, item)

    def drink_potion(self, potion):
        potion_type = getattr(potion, 'potion_type')
        points = getattr(potion, 'points')

        if potion_type == 'mana':
            self.take_mana(points)

        if potion_type == 'health':
            self.take_healing(points)

    # Attack

    def get_strongest_mean(self):  # weapon VS spell
        weapon_damage = getattr(self.weapon, 'damage') if self.weapon else 0
        spell_damage = getattr(self.spell, 'damage') if self.spell and self.can_cast() else 0

        if weapon_damage == 0 and spell_damage == 0:
            return None
        elif weapon_damage >= spell_damage:
            return self.weapon
        else:
            self.mana -= getattr(self.spell, 'mana_cost')
            return self.spell

    # Static

    @staticmethod
    def validate_input_human(health, mana):
        if type(health) is not int and type(health) is not float:
            raise TypeError('Health must be of "int" / "float" type.')
        elif type(mana) is not int:
            raise TypeError('Mana must be of "int" type.')
        elif health < 0:
            raise Exception('Health cannot be less than 0.')
        elif mana < 0:
            raise Exception('Mana cannot be less than 0.')


if __name__ == '__main__':
    h = Human(50, 30)
    a = Armor('a', 50)
    h.equip_item(a)
    print(h.armor)
