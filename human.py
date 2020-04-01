# human.py

from weapon import Weapon
from spell import Spell

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

    # Public

    def is_alive(self):                                                         
        return self.health != 0

    def can_cast(self):                                                                     
        if self.spell is None:
            print("You don't know any spells.")
            return False
        else:
            return self.mana >= getattr(self.spell, 'mana_cost')

    def get_health(self):                                                       
        return self.health

    def get_mana(self):                                                         
        return self.mana

    def take_healing(self, healing_points):                                     
        if self.health == 0:
            return False
        elif healing_points + self.health > self.max_health:
            self.health = self.max_health
        else:
            self.health += healing_points

    def take_mana(self, mana_points):                                           
        if self.mana + mana_points > self.max_mana:
            self.mana = self.max_mana
        else:
            self.mana += mana_points

    def take_damage(self, damage):                                              
        if type(damage) is not float and type(damage) is not int:
            raise TypeError('Damage must be of "int" / "float" type.')

        if damage > self.health:
            self.health = 0
        else:
            self.health -= damage

    def equip(self, weapon):    
        if type(weapon) is not Weapon:
            raise TypeError('Argument must be of "Weapon" type.')
        
        self.weapon = weapon

    def learn(self, spell):   
        if type(spell) is not Spell:
            raise TypeError('Argument must be of "Spell" type.')
        
        self.spell = spell

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