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

    def attack(self, by = None):                                                            
        if type(by) is not str: 
            raise TypeError('Means of attack must be specified.')

        if by is 'weapon':
            if self.weapon is None:
                return 0
            else:
                return getattr(self.weapon, 'damage') 
        elif by is 'magic':
            if self.spell is None:
                return 0
            elif getattr(self.spell, 'mana_cost') > self.mana:
                print('Not enough mana to cast the spell.')
                return 0
            else:
                return getattr(self.spell, 'damage')
                # TODO: Handling cast_range.
        else:
            raise Exception('Unrecognized means of attack.')

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