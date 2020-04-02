# human.py

from weapon import Weapon
from spell import Spell
from armor import Armor

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

    def is_alive(self):                                                         
        return self.health != 0

    def can_cast(self):    # TODO
        if self.spell:
            return self.mana >= getattr(self.spell, 'mana_cost')
        else:
            return False

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

    def take_damage(self, damage):                                         
        if type(damage) is not float and type(damage) is not int:
            raise TypeError('Damage must be of "int" / "float" type.')

        armor_points = 0    

        if self.armor:
            armor_points = getattr(self.armor, 'armor_points')

        if damage > armor_points:
            damage -= armor_points

            self.health = (self.health - damage) if damage < self.health else 0
                
    def equip(self, weapon=None, armor=None): # TODO така или отделни ф-ии equip_armor/equip_weapon
        if weapon:
            if type(weapon) is not Weapon:
                raise TypeError('Argument must be of "Weapon" type.')

            if self.weapon:
                if self.weapon < weapon:
                    self.weapon = weapon
            else:
                self.weapon = weapon       
        if armor:
            if type(armor) is not Armor:
                raise TypeError('Argument must be of "Armor" type.')
            if self.armor:
                if self.armor < armor:
                    self.armor = armor
            else:
                self.armor = armor   

    def learn(self, spell):   
        if type(spell) is not Spell:
            raise TypeError('Argument must be of "Spell" type.')
        if self.spell:
            if self.spell < spell:
                    self.spell = spell
        else:
            self.spell = spell        

    def attack_with_strongest_mean(self):
        pass       

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