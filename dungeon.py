# dungeon.py

from random import randint

from hero import Hero
from enemy import Enemy
from weapon import Weapon
from spell import Spell
from armor import Armor
from potion import Potion
import collections

def get_file_content(filename):  # in utils
    with open(filename, 'r') as f:
        return f.readlines()


class Dungeon:
    # Constructor

    def __init__(self, map_file_name, treasure_file_name='treasures.txt'):
        self.validate_input_dungeon(map_file_name)
        self.map = self.init_map(map_file_name)
        self.map_size_x = len(self.map)
        self.map_size_y = len(self.map[0])

        self.hero = None
        self.hero_coordinates = {'x': -1, 'y': -1}

        self.last_step = None
        self.saved_hero = None

        self.treasures = self.init_treasures(treasure_file_name)

    @staticmethod  # in utils?
    def init_map(filename):
        dungeon_map = get_file_content(filename)
        return [[char for char in row][:-1] for row in dungeon_map]

    @staticmethod  # in utils?
    def init_treasures(filename):
        all_lines = get_file_content(filename)
        treasures = []

        for line in all_lines:
            line = line.split(' ')
            treasure_type = eval(line[0])

            if treasure_type in [Potion, Weapon, Spell, Armor]:
                treasures.append(treasure_type.from_list(line[1:]))

        return treasures

    # Public

    def print_map(self):                                                        # DONE
        for row in self.map:
            print(''.join(row))

    def spawn(self, hero):                                                      # DONE
        if type(hero) is not Hero:
            raise TypeError('Argument must be of "Hero" type.')

        assert not self.hero, 'Cannot have more than 1 hero in the dungeon.'

        for row in range(0, len(self.map)):
            for col in range(0, len(self.map[row])):
                if self._check_if_spawn_point(row, col):
                    self.hero = hero
                    self.saved_hero = hero

                    self.hero_coordinates['x'] = row
                    self.hero_coordinates['y'] = col

                    self.map[row][col] = 'H'
                    self.last_step = '.'
                    return True

        return False

    def move_hero(self, direction):
        way = {'up': {'x': -1, 'y': 0},
               'down': {'x': 1, 'y': 0},
               'left': {'x': 0, 'y': -1},
               'right': {'x': 0, 'y': 1}}

        if type(direction) is not str:
                raise TypeError('Direction must be of "str" type.')
        elif direction not in way.keys():
                raise Exception('Unrecognized direction.')
        elif not self.hero:
                raise Exception('No hero on the map.')

        new_pos_x = self.hero_coordinates['x'] + way[direction]['x']
        new_pos_y = self.hero_coordinates['y'] + way[direction]['y']

        self.hero.regenerate_mana()  # Handle mana regen 1

        if self._check_if_invalid_position(new_pos_x, new_pos_y) or \
           self._check_if_obstacle(new_pos_x, new_pos_y):
            print('You cannot go there!')
            return False

        elif self._check_if_walkable_path(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            return True

        elif self._check_if_treasure(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('Found treasure!')
            self.pick_treasure()
            return True

        elif self._check_if_enemy(new_pos_x, new_pos_y):
            enemy = Enemy(50, 50, 20)

            print('A fight is started between:')
            print(f'Our hero - {self.hero.known_as()} (health = {self.hero.get_health()}, mana = {self.hero.get_mana()})\nand')

            print(f'Enemey(health={enemy.get_health()}, mana={enemy.get_mana()}, damage={getattr(enemy,"damage")})')

            self._fight(enemy)

            if self.hero.is_alive():
                print('Enemy is dead!')

                self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            else:
                print('Hero died!')

                self.map[self.hero_coordinates['x']][self.hero_coordinates['y']] = self.last_step
                self.hero = None

                if self.spawn(self.saved_hero):
                    print('Hero Respawned.')
                else:
                    print('Hero could not respawn.')
                    print('-GAME OVER-')

        elif self._check_if_spawn_point(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, 'S')
            return True

        elif self._check_if_gateway(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('CONGRATULATIONS!\nYOU WON!')
            return True

    def _fight(self, enemy):                                                  # TODO: Test
        for index in range(0, 5):
            attack_type = {Spell: 'casts a', Weapon: 'hits with'}
            self.hero.regenerate_mana()

            hero_weapon = self.hero.attack()
            if hero_weapon is not None:
                hero_weapon_name = getattr(hero_weapon, 'name')
                hero_weapon_damage = getattr(hero_weapon, 'damage')

            enemy_weapon = enemy.attack()
            enemy_weapon_name = getattr(enemy_weapon, 'name')
            enemy_weapon_damage = getattr(enemy_weapon, 'damage')

            if hero_weapon is None:
                print("Hero doesn't have a weapon. He didn't hit the enemy.")
            else:
                print(f'Hero {attack_type[type(hero_weapon)]} {hero_weapon_name}, hits enemy for {hero_weapon_damage}.')
                enemy.take_damage(hero_weapon_damage)

            print(f'Enemy health is {enemy.get_health()}.')

            if not enemy.is_alive():
                return

            print(f'Enemy {attack_type[type(enemy_weapon)]} {enemy_weapon_name}, hits Hero for {enemy_weapon_damage}.')
            self.hero.take_damage(enemy_weapon_damage)
            print(f'Hero health is {self.hero.get_health()}.')

            if not self.hero.is_alive():
                return

        print('Hero got tired and let his guard down.')
        setattr(self.hero, 'health', 0)
        return

    def hero_attack(self, by): # TODO: TEST
        if by == 'spell':
            casting_range = getattr(getattr(self.hero, 'spell'), 'cast_range')
            
            enemy_pos = self.check_for_enemy(casting_range)
            
            if enemy_pos['x'] != -1 and enemy_pos['y'] != -1:
                enemy = Enemy(50, 50, 20)

                path = self.bfs((enemy_pos['x'], enemy_pos['y']))

                print('A fight is started between:')
                print(f'Our hero - {self.hero.known_as()} (health = {self.hero.get_health()}, mana = {self.hero.get_mana()})\nand')

                print(f'Enemey(health={enemy.get_health()}, mana={enemy.get_mana()}, damage={getattr(enemy,"damage")})')    
                
                for elem in path:
                    self.hero.regenerate_mana()

                    hero_weapon = self.hero.attack(by = 'magic')

                    if type(hero_weapon) == Spell: # FIX!!!
                        hero_weapon_name = getattr(hero_weapon, 'name')
                        hero_weapon_damage = getattr(hero_weapon, 'damage')
                        
                        print(f'Hero casts a {hero_weapon_name}, hits enemy for {hero_weapon_damage}.')
                        
                        enemy.take_damage(hero_weapon_damage)

                    else:
                        print('Hero is out of mana.') # TODO: check weapon 

                    print('Enemy moved one square.')
                    
                    if self.map[elem[0]][elem[1]] == 'T':
                        print('Enemy found treasure!')
                        treasure = self.treasures[randint(0, len(self.treasures) - 1)]
                        treasure.equip_to(enemy)
                self._fight(enemy)

                if self.hero.is_alive():
                    print('Enemy is dead!')
                else:
                    print('Hero died!')

                    self.map[self.hero_coordinates['x']][self.hero_coordinates['y']] = self.last_step
                    self.hero = None

                    if self.spawn(self.saved_hero):
                        print('Hero Respawned.')
                    else:
                        print('Hero could not respawn.')
                        print('-GAME OVER-')

            else:
                print(f'Nothing in casting range {casting_range}.')
        else:
            raise Exception('Unrecognized means of attack.')

    def check_for_enemy(self, cast_range):
        enemy_position = {'x': -1, 'y': -1}

        way = {'up': {'x': -1, 'y': 0},
               'down': {'x': 1, 'y': 0},
               'left': {'x': 0, 'y': -1},
               'right': {'x': 0, 'y': 1}}

        for i in range(0, cast_range):
            for direction in way.keys():
                x = self.hero_coordinates['x'] + (i * way[direction]['x'])
                y = self.hero_coordinates['y'] + (i * way[direction]['y'])
                if not self._check_if_invalid_position(x, y):
                    if self._check_if_enemy(x, y):
                        enemy_position = {'x': x, 'y': y}
                        return enemy_position

        return enemy_position

    def bfs(self, start):
        queue = collections.deque([[start]])
        seen = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self.map[x][y] == 'H':
                return path
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if 0 <= x2 < self.map_size_x and 0 <= y2 < self.map_size_y and self.map[x2][y2] != '#' and (y2, x2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((y2, x2))

    # Help Enemy move to Hero

    def _move_enemy_towards_hero(self, enemy_x, enemy_y):                       # TODO: Implement + Test
        path = self.bfs((enemy_x, enemy_y))
        print(path)

    def pick_treasure(self):                                                    # DONE
        treasure = self.treasures[randint(0, len(self.treasures) - 1)]
        treasure.equip_to(self.hero)

    # Help functions for move

    def _check_if_invalid_position(self, new_pos_x, new_pos_y):                 # DONE
        return new_pos_x < 0 or new_pos_x >= self.map_size_x or \
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
        self.map[self.hero_coordinates['x']][self.hero_coordinates['y']] = self.last_step
        self.last_step = current_step

        self.map[new_pos_x][new_pos_y] = 'H'
        self.hero_coordinates['x'] = new_pos_x
        self.hero_coordinates['y'] = new_pos_y

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
            print('No such file.', filename)

h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

w = Weapon(name="The Axe of Destiny", damage=20)
h.equip(w)

s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
h.equip(s)

map = Dungeon("level1.txt")
map.spawn(h)
map.print_map()
# NOVI TESTOVE HAHA
map.hero_attack(by='spell')
map.move_hero('right')
map.print_map()
map.hero_attack(by='spell')
map.move_hero('down')
map.hero_attack(by='spell') 
map.move_hero('down')
map.hero_attack(by='spell') 
map.print_map()
map.move_hero('down')
map.move_hero('down')
map.print_map()
map.hero_attack(by='spell')
#map.print_map()

'''
map.move_hero("right")
map.print_map()

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
# map.print_map()
'''
