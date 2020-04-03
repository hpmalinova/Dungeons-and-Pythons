# dungeon.py

from hero import Hero
from enemy import Enemy
from weapon import Weapon
from spell import Spell
from potion import Potion
from weapon import Weapon
from armor import Armor
from random import randint

class Dungeon:
    # Constructor

    def __init__ (self, filename):                                              # TODO: Add Treasures
        self.validate_input_dungeon(filename)
        self.map = []
            
        with open(filename, 'r') as f:
            while True: 
                line = f.readline()
                        
                if not line: 
                    break
                else:
                    line = list(line)
                    line = line[:-1]
                    self.map.append(line)
    
        self.saved_hero = None
        self.hero = None
        self.last_step = None
        self.pos_x = None
        self.pos_y = None
        self.map_size_x = len(self.map)
        self.map_size_y = len(self.map[0])
        self.treasures = self.__initialize_treasures('treasures.txt')

    # Public

    def print_map(self):                                                        # DONE
        for elem in self.map:
            print(''.join(elem))

    def spawn(self, hero):                                                      # DONE
        if type(hero) is not Hero:
            raise TypeError('Argument must be of "Hero" type.')
        elif self.hero is not None:
            raise Exception('Cannot have more than 1 hero in the dungeon.')

        for row in range(0, len(self.map)):
            for col in range(0, len(self.map[row])):
                if self.map[row][col] == 'S':
                    self.hero = hero
                    self.saved_hero = hero
                    self.pos_x = col
                    self.pos_y = row
                    self.map[row][col] = 'H'
                    self.last_step = '.'
                    return True
        print('-GAME OVER-')
        return False

    def move_hero(self, direction):
        way = { 'up': {'x': -1, 'y': 0}, 'down': {'x': 1, 'y': 0}, 
                'left': {'x': 0, 'y': -1}, 'right': {'x': 0, 'y': 1} }
            
        if type(direction) is not str:
                raise TypeError('Direction must be of "str" type.')
        elif direction not in way.keys():
                raise Exception('Unrecognized direction.')
        elif self.hero == None:
                raise Exception('No hero on the map.')

        new_pos_x = self.pos_x + way[direction]['x']
        new_pos_y = self.pos_y + way[direction]['y']
            
        if  self._check_if_invalid_position(new_pos_x, new_pos_y) or \
            self._check_if_obstacle(new_pos_x, new_pos_y):
            
            print('You cannot go there!')
            return False
                
        if self._check_if_walkable_path(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            return True
            
        if self._check_if_treasure(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('Found treasure!')
            self.pick_treasure()
            return True
                
        if self._check_if_enemy(new_pos_x, new_pos_y):
            enemy = Enemy(50, 50, 20)

            print('A fight is started between:')
            print(f'Our hero - {self.hero.known_as()}(health = {self.hero.get_health()}, mana = {self.hero.get_mana()})\nand\n')
            print(f'Enemey(health={enemy.get_health()}, mana={enemy.get_mana()}, damage={getattr(enemy,"damage")})')
            
            self._fight(enemy)

            if self.hero.is_alive():
                print('Enemy is dead!')

                self.__move_hero_to_position(new_pos_x, new_pos_y, '.')

                return True 
            else:
                print('Hero died!')

                self.map[self.pos_x][self.pos_y] = self.last_step
                self.hero = None

                if self.spawn(self.saved_hero):
                    print('Hero Respawned.')
                else:
                    print('Hero could not respawn.')

                return False
                    
        if self._check_if_spawn_point(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, 'S')
            return True
     
        if self._check_if_gateway(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('CONGRATULATIONS!\nYOU WON!')
            return True

    def _fight(self, encountered_enemy):                                         # TODO: Test
        while self.hero.is_alive() and encountered_enemy.is_alive():
            encountered_enemy.take_damage(self.hero.attack_with_strongest_mean())
            self.hero.take_damage(encountered_enemy.attack_with_strongest_mean())


    def hero_attack(self, by):                                                  # TODO: Implement + Test
        # IF TRUE : MAKE ENEMY, WHILE WALK, TAKE DAMAGE, CALL FIGHT
        pass

    def pick_treasure(self):                                                    # DONE
        treasure = self.treasures[randint(0, len(self.treasures) - 1)] 
        test = Armor('pesho', 10)
        print(test)
        treasure.equip_to(self.hero)

    # Help Enemy move to Hero:

    def _move_enemy_towards_hero(self, enemy_x, enemy_y):
        pass

    # Help initialize treasures

    def __initialize_treasures(self, filename):                                # TODO: Test
        treasures = []

        with open(filename, 'r') as f:
           while True:  
                line = f.readline()
                if not line: 
                    break
                else:
                    line_list = list(line.split())
                    if line_list[0] == 'Potion':
                        treasures.append(Potion(line_list[1], int(line_list[2])))
                    elif line_list[0] == 'Weapon':
                        treasures.append(Weapon(line_list[1], int(line_list[2])))
                    elif line_list[0] == 'Armor':
                        treasures.append(Armor(line_list[1], int(line_list[2])))
                    else:
                        treasures.append(Spell(line_list[1], int(line_list[2]), int(line_list[3]), int(line_list[4])))
        return treasures
            

    # Help functions for move:
        
    def _check_if_invalid_position(self, new_pos_x, new_pos_y):                 # DONE
        return new_pos_x < 0 or new_pos_x >= self.map_size_x or\
                new_pos_y < 0 or new_pos_y >= self.map_size_y
        
    def _check_if_obstacle(self, new_pos_x, new_pos_y):                         # DONE
        return self.map[new_pos_x][new_pos_y] == '#'    
    
    def _check_if_walkable_path(self, new_pos_x, new_pos_y):                    # DONE
        return self.map[new_pos_x][new_pos_y] == '.'
        
    def _check_if_treasure(self, new_pos_x, new_pos_y):                         # DONE
        return self.map[new_pos_x][new_pos_y] == 'T'    
    
    def _check_if_enemy(self, new_pos_x, new_pos_y):                            # DONE
        return self.map[new_pos_x][new_pos_y] == 'E'
        
    def _check_if_spawn_point(self, new_pos_x, new_pos_y):                      # DONE
        return self.map[new_pos_x][new_pos_y] == 'S'

    def _check_if_gateway(self, new_pos_x, new_pos_y):                          # DONE 
        return self.map[new_pos_x][new_pos_y] == 'G'
    
    def __move_hero_to_position(self, new_pos_x, new_pos_y, current_step):      # DONE
        self.map[self.pos_x][self.pos_y] = self.last_step
        self.last_step = current_step
                
        self.map[new_pos_x][new_pos_y] = 'H'
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y

    # Static

    @staticmethod
    def validate_input_dungeon(filename):
        if type(filename) is not str:
            raise TypeError('Filename must be of "str" type.')
       
        try:
            with open(filename, 'r') as f:
                len_line = len(f.readline())

                while True: 
                    line = f.readline()
                    if not line: 
                        break
                    elif len(line) != len_line:
                        raise Exception('Map must be rectangular.')
                    
        except FileNotFoundError:
            print('No such file.')


#Improvised test :

h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

w = Weapon(name="The Axe of Destiny", damage=20)

h.equip(w)

s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

h.equip(s)                                                                  # It was 'learn'

map = Dungeon("level1.txt")

map.spawn(h)

map.print_map()

map.move_hero("right")

map.move_hero("down")

map.print_map()

# map.hero_attack(by="spell")

map.move_hero("down")

map.move_hero("down")

map.print_map()

map.move_hero("right")

map.print_map()

map.move_hero("right")
map.move_hero("right")
map.move_hero("right")
map.move_hero("up")
map.move_hero("up")
map.move_hero("up")
map.move_hero("right")
map.move_hero("right")
map.move_hero("right")
map.move_hero("right")
map.move_hero("down")
map.move_hero("down")
map.move_hero("down")
map.move_hero("down")
#map.print_map()
