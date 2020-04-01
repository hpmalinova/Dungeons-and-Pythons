# human.py

class Human:
    # Constructor

    def __init__(self, health, mana):                                           # DONE
        self.max_health = health
        self.max_mana = mana

        self.health = health
        self.mana = mana

    # Public

    def is_alive(self):                                                         # DONE
        return self.health != 0

    def can_cast(self):
        pass

    def get_health(self):                                                       # DONE
        return self.health

    def get_mana(self):                                                         # DONE
        return self.mana

    def take_healing(self, healing_points):                                     # DONE
        if self.health == 0:
            return False
        elif healing_points + self.health > self.max_health:
            self.health = self.max_health
        else:
            self.health += healing_points

    def take_mana(self, mana_points):                                           # DONE
        if self.mana + mana_points > self.max_mana:
            self.mana = self.max_mana
        else:
            self.mana += mana_points

    def attack(self):
        pass

    def take_damage(self, damage):                                              # DONE
        if type(damage) is not float and type(damage) is not int:
            raise TypeError('Damage must be of "int" / "float" type.')

        if damage > self.health:
            self.health = 0
        else:
            self.health -= damage

    # Static

    @staticmethod
    def validate_input(health, mana):                                           # DONE
        if type(health) is not int and type(health) is not float:
            raise TypeError('Health must be of "int" / "float" type.')
        elif type(mana) is not int:
            raise TypeError('Mana must be of "int" type.')