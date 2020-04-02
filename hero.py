# hero.py

from human import Human

class Hero(Human):
    # Constructor

    def __init__(self, name, title, health, mana, mana_regeneration_rate):
        super().__init__(health, mana)

        self.validate_input_hero(name, title, mana_regeneration_rate)

        self.name = name
        self.title = title
        self.mana_regeneration_rate = mana_regeneration_rate

    # Public

    def known_as(self):                                                                     
        return f'{self.name} the {self.title}'

    def attack(self, by = None): # TODO: if no arguments - attack with the strongest attack                                                     
        if type(by) is not str: 
            raise TypeError('Means of attack must be specified.')

        if by is 'weapon':
            return self.__attack_by_weapon()
        if by is 'magic':
            return self.__attack_by_magic()
        
        raise Exception('Unrecognized means of attack.')

    def __get_stronger_attack(self): #TODO
        pass

    def __attack_by_weapon(self):
        if self.weapon is None:
            return 0
        else:
            return getattr(self.weapon, 'damage')         

    def __attack_by_magic(self):
        if not self.spell:
            print("You don't know any spells.")
            return 0
        if self.can_cast():
            self.mana -= getattr(self.spell, 'mana_cost')
            return getattr(self.spell, 'damage')
        else: 
            print('Not enough mana to cast the spell.')
            return 0   

        # TODO: Handling cast_range.
   

    def take_mana(self, mana_points):  
        if self.mana + mana_points > self.max_mana:
            self.mana = self.max_mana
        else:
            self.mana += mana_points      

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
            raise Exception('Mana regeneration rate cannot be negative.')

    # Equipment

    def drink_potion(self, potion):
        if getattr(potion, 'potion_type') == 'mana':
            self.take_mana(potion.points)

        if getattr(potion, 'potion_type') == 'health':
            self.take_healing(potion.points)      