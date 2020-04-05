# dungeon.py

from random import randint

from hero import Hero
from enemy import Enemy
from weapon import Weapon
from spell import Spell
from armor import Armor
from potion import Potion


def get_file_content(filename):  # in utils
    with open(filename, 'r') as f:
        return f.readlines()


class Dungeon:
    # Constructor

    def __init__(self, map_file_name, treasure_file_name='treasures.txt'):
        self.validate_input_dungeon(map_file_name)
        self.map = self.init_map(map_file_name)

        self.hero = None
        self.hero_coordinates = {'x': -1, 'y': -1}

        self.last_step = None
        self.saved_hero = None

        self.treasures = self.init_treasures(treasure_file_name)

    @staticmethod
    def init_map(filename):
        dungeon_map = get_file_content(filename)
        return [[char for char in row][:-1] for row in dungeon_map]

    @staticmethod
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

    def print_map(self):
        for row in self.map:
            print(''.join(row))

    def spawn(self, hero):  # returns True/ False
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
            print('Start a new game!')
            return

        new_pos_x = self.hero_coordinates['x'] + way[direction]['x']
        new_pos_y = self.hero_coordinates['y'] + way[direction]['y']

        self.hero.regenerate_mana()

        if self._check_if_invalid_position(new_pos_x, new_pos_y) or \
           self._check_if_obstacle(new_pos_x, new_pos_y):
            print('You cannot go there!')
            return

        print('==================================================================')

        if self._check_if_walkable_path(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('Successfully moved.')

        elif self._check_if_treasure(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            self.pick_treasure(self.hero)

        elif self._check_if_spawn_point(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, 'S')
            print('Successfully moved.')

        elif self._check_if_gateway(new_pos_x, new_pos_y):
            self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            print('CONGRATULATIONS!\nYOU WON!')

        elif self._check_if_enemy(new_pos_x, new_pos_y):
            enemy = Enemy(50, 50, 20)

            fight_result = ''

            fight_result += '*** A fight is started between: ***\n'
            fight_result += (f'Our hero - {self.hero.known_as()} (health = {self.hero.get_health()}, '
                             f'mana = {self.hero.get_mana()}) and\n')
            fight_result += (f'Enemy (health = {enemy.get_health()}, mana = {enemy.get_mana()}, '
                             f'damage = {getattr(enemy,"damage")})\n')
            fight_result += '***********************************\n'
            fight_result += self._fight(enemy)

            if self.hero.is_alive():
                fight_result += 'Enemy is dead!'
                self.__move_hero_to_position(new_pos_x, new_pos_y, '.')
            else:
                fight_result += 'Hero died!\n'

                self.map[self.hero_coordinates['x']][self.hero_coordinates['y']] = self.last_step
                self.hero = None

                if self.spawn(self.saved_hero):
                    fight_result += 'Hero Respawned.'
                else:
                    fight_result += 'Hero could not respawn.\n--- GAME OVER ---'

            print(fight_result)

        if self.hero:
            self.print_map()

    def _fight(self, enemy):
        fight_result = ''

        while True:
            if not getattr(self.hero, 'weapon') and not getattr(self.hero, 'spell'):
                fight_result += ('Hero doesn`t have a weapon and doesn`t know a spell.\n'
                                 'He doesn`t stand a chance against the enemy.\n')
                setattr(self.hero, 'health', 0)
                return fight_result

            self.hero.regenerate_mana()

            enemy_damage_taken, hero_weapon, add_to_string = self.attack(self.hero, enemy)
            fight_result += add_to_string

            if not enemy.is_alive():
                return fight_result

            hero_damage_taken, enemy_weapon, add_to_string = self.attack(enemy, self.hero)
            fight_result += add_to_string

            if not self.hero.is_alive():
                return fight_result

            if hero_damage_taken == 0 and enemy_damage_taken == 0 and \
               type(hero_weapon) == Weapon and type(enemy_weapon) == Weapon:
                fight_result += 'Hero got tired and let his guard down.\n'
                setattr(self.hero, 'health', 0)
                return fight_result

    @staticmethod
    def attack(attacker, defender):  # self.hero or enemy
        weapon = attacker.attack()
        weapon_type = type(weapon)
        weapon_name = getattr(weapon, 'name')
        weapon_dmg = getattr(weapon, 'damage')

        damage_taken = defender.take_damage(weapon_dmg)
        defender_armor = getattr(defender, 'armor')

        attack_type = {Spell: 'casts a', Weapon: 'hits with'}

        result = ''
        result += (f'{type(attacker).__name__} {attack_type[weapon_type]} '
                   f'{weapon_name}, tries to deal {weapon_dmg} damage.\n')

        if defender_armor is not None:
            defender_name = type(defender).__name__
            defender_armor_name = getattr(defender_armor, 'name')
            defender_armor_points = getattr(defender_armor, 'armor_points')

            result += f'{defender_name}`s {defender_armor_name} took {defender_armor_points } of the damage.\n'

        result += f'{type(defender).__name__} health is {defender.get_health()}.\n'

        return (damage_taken, weapon, result)

    def hero_attack(self, by):
        if self.hero is None:
            print('No hero on the map. Try to spawn a new one.')
            return

        if by == 'magic':  # Fix
            casting_range = self.hero.get_spell_cast_range()

            if casting_range == -1:
                print('Hero doesn`t know any spells')
                return
            elif not self.hero.can_cast():
                print('Hero has no mana to cast the spell')
                return
            else:
                enemy_pos = self.check_for_enemy(casting_range)

                if enemy_pos['x'] != -1 and enemy_pos['y'] != -1:
                    enemy = Enemy(50, 50, 20)

                    path = self.bfs((enemy_pos['x'], enemy_pos['y']))

                    print('A fight is started between:')
                    print(f'Our hero - {self.hero.known_as()} (health = {self.hero.get_health()}, '
                          f'mana = {self.hero.get_mana()})\nand')
                    print(f'Enemy(health={enemy.get_health()}, mana={enemy.get_mana()}, '
                          'damage={getattr(enemy,"damage")})')

                    for elem in path:
                        self.hero.regenerate_mana()

                        hero_weapon = self.hero.attack(by='magic')

                        if type(hero_weapon) == Spell:
                            hero_weapon_name = getattr(hero_weapon, 'name')
                            hero_weapon_damage = getattr(hero_weapon, 'damage')

                            print(f'Hero casts a {hero_weapon_name}, hits enemy for {hero_weapon_damage}.')

                            enemy.take_damage(hero_weapon_damage)
                        else:
                            print('Hero is out of mana.')

                        if not enemy.is_alive():
                            print('Enemy is dead.')
                            return
                        else:
                            print('Enemy moved one square.')

                        if self.map[elem[0]][elem[1]] == 'T':
                            self.pick_treasure(enemy)

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
                    print(f'No enemy in casting range: {casting_range}.')
        else:
            raise Exception('Unrecognized means of attack.')

    def check_for_enemy(self, cast_range):
        enemy_position = {'x': -1, 'y': -1}

        way = {'up': {'x': -1, 'y': 0},
               'down': {'x': 1, 'y': 0},
               'left': {'x': 0, 'y': -1},
               'right': {'x': 0, 'y': 1}}

        for i in range(0, cast_range + 1):
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
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < self.map_size_x and 0 <= y2 < self.map_size_y and \
                        self.map[x2][y2] != '#' and (y2, x2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((y2, x2))

    def pick_treasure(self, winner):                                                    # DONE
        treasure = self.treasures[randint(0, len(self.treasures) - 1)]
        treasure.equip_to(winner)
        print(f'{type(winner).__name__} finds a treasure: ', treasure)

    # Help functions for move

    def _check_if_invalid_position(self, new_pos_x, new_pos_y):                 # DONE
        return new_pos_x < 0 or new_pos_x >= len(self.map) or \
            new_pos_y < 0 or new_pos_y >= len(self.map[0])

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


##############################################
h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

w = Weapon(name="The Axe of Destiny", damage=20)
h.equip(w)

s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
h.equip(s)

map = Dungeon("level1.txt")
map.spawn(h)

map.move_hero("right")

map.move_hero("down")

map.hero_attack(by="magic")

map.move_hero("down")
map.move_hero("down")

map.move_hero("right")

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
