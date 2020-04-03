# dungeon.py

from hero import Hero
from weapon import Weapon
from spell import Spell
from random import randint


class Dungeon:
    # Constructor

    def __init__ (self, filename):                                              # TODO: Add Enemies and Treasures
        self.validate_input_dungeon(filename)

        self.map = []
        
        try:
            with open(filename, 'r') as f:
                while True: 
                    line = f.readline()
                    
                    if not line: 
                        break
                    else:
                        line = list(line)
                        line = line[:-1]
                        self.map.append(line)
        except FileNotFoundError:
            print('No such file.')
        
        self.hero = None
        self.last_step = None
        self.pos_x = None
        self.pos_y = None
        self.map_size_x = len(self.map)
        self.map_size_y = len(self.map[0])
        # TODO: Enemies
        # TODO: Treasures

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
                    self.pos_x = col
                    self.pos_y = row
                    self.map[row][col] = 'H'
                    self.last_step = '.'
                    return True
        print('-GAME OVER-')
        return False

    def move_hero(self, direction):                                             # TODO: Test
        # way = {'up' : {'x': -1, 'y': 0}, 'down' : {'x': 1, 'y': 0}, 'left' : {'x': 0, 'y': -1}, 'right' : {'x': 0, 'y': 1}
        # way[direction][x]
        way = {'up': (-1, 0), 'down':(1, 0), 'left':(0, -1), 'right':(0, 1)}
            
        if type(direction) is not str:
                raise TypeError('Direction must be of "str" type.')
        elif direction not in way.keys():
                raise Exception('Unrecognized direction.')
            elif self.hero == None:
                raise Exception('No hero on the map.')

        new_pos_x = self.pos_x + way[direction][0]
        new_pos_y = self.pos_y + way[direction][1]
            
        if  self.__check_if_invalid_position(new_pos_x, new_pos_y) or \
            self.__check_for_obstacle(new_pos_x, new_pos_y):
            
            print('You cannot go there!')
            return False
                
        if self.__check_if_walkable_path(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            return True
            
        if self.__check_if_treasure(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('Found treasure!')
            self.pick_treasure() # po uslovie e pick treasure
            return True
                
        if self.__check_if_enemy(new_pos_x, new_pos_y):
            self.fight() # ruk da pishem dali e umrql ili ne? // return true/false

            if self.hero.is_alive():
                self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
                        return True 
            else:
                self.map[self.pos_x][self.pos_y] = self.last_step
                    
                if self.spawn(self.hero):
                    print('Hero Respawned.')
                else:
                    print('Hero could not respawn.')

                return False
                    
        if self.__check_if_spawn_point(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, 'S')
            return True
     
        if self.__check_if_gateway(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('CONGRATULATIONS!\nYOU WON!')
            return True

    def fight(self):                                                            # TODO: Implement + Test
        pass

    def hero_attack(self, by):                                                  # TODO: Implement + Test
        pass

    def pick_treasure(self):                                                    # TODO: Implement + Test
        pass

    # Help functions for move:
        
    def __check_if_invalid_position(self, new_pos_x, new_pos_y):
    return new_pos_x < 0 or new_pos_x >= self.map_size_x or\
        new_pos_y < 0 or new_pos_y >= self.map_size_y
        
    def __check_if_obstacle(self, new_pos_x, new_pos_y):
    return self.map[new_pos_x][new_pos_y] == '#'    
    
    def __check_if_walkable_path(self, new_pos_x, new_pos_y):
    return self.map[new_pos_x][new_pos_y] == '.'
        
    def __check_if_treasure(self, new_pos_x, new_pos_y):
        return self.map[new_pos_x][new_pos_y] == 'T'    
    
    def __check_if_enemy(self, new_pos_x, new_pos_y):
    return self.map[new_pos_x][new_pos_y] == 'E'
        
    def __check_if_spawn_point(new_pos_x, new_pos_y):
    return self.map[new_pos_x][new_pos_y] == 'S'

    def __check_if_gateway(self, new_pos_x, new_pos_y):
    return self.map[new_pos_x][new_pos_y] == 'G'
    
    def __move_hero_to_position(new_pos_x, new_pos_y, current_step):
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
        # TODO: Handling lines check (size of map)

'''
Improvised test :)

h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

w = Weapon(name="The Axe of Destiny", damage=20)

h.equip(w)

s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

h.learn(s)

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
'''