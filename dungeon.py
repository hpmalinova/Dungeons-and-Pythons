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
            print(f'Our hero - {self.hero.known_as()} \
                (health = {self.hero.get_health()}, mana = {self.hero.get_mana()})\nand')

            print(f'Enemey(health={enemy.get_health()}, \
                mana={enemy.get_mana()}, damage={getattr(enemy,"damage")})')

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

    def _fight(self, enemy):
        while True:
            string_result = ''

            if not getattr(self.hero, 'weapon') and not getattr(self.hero, 'spell'):
                string_result += 'Hero doesn`t have a weapon and doesn`t know a spell.\n \
                                  He doesn`t stand a chance against the enemy.'
                setattr(self.hero, 'health', 0)
                return string_result

            self.hero.regenerate_mana()

            enemy_damage_taken, hero_weapon, add_to_string = self.attack(self.hero, enemy)
            string_result += add_to_string

            if not enemy.is_alive():
                return string_result

            hero_damage_taken, enemy_weapon, add_to_string = self.attack(enemy, self.hero)
            string_result += add_to_string

            if not self.hero.is_alive():
                return string_result

            if hero_damage_taken == 0 and enemy_damage_taken == 0 and \
               type(hero_weapon) == Weapon and type(enemy_weapon) == Weapon:
                string_result += 'Hero got tired and let his guard down.'
                setattr(self.hero, 'health', 0)
                return string_result

    def attack(attacker, defender):  # self.hero or enemy
        weapon = attacker.attack()
        weapon_type = type(weapon)
        weapon_name = getattr(weapon, 'name')
        weapon_dmg = getattr(weapon, 'damage')

        damage_taken = defender.take_damage(weapon_dmg)
        defender_armor = getattr(defender, 'armor')

        attack_type = {Spell: 'casts a', Weapon: 'hits with'}

        result = ''
        result += f'{type(attacker).__name__} {attack_type[weapon]} {weapon_name}, \
                    tries to deal {weapon_dmg} damage.\n'
        if defender_armor:
            result += '{type(defender).__name__}`s {getattr(defender_armor, 'name')} took \
                               {getattr(defender_armor, 'armor_points')} of the damage'

        result += f'{type(defender).__name__} health is {defender.get_health()}.'

        return (damage_taken, weapon, result)


    def hero_attack(self, by):  # TODO: Implement + Test
        pass
        # IF TRUE : WHILE WALK, TAKE DAMAGE, CALL FIGHT

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

                if self._check_if_enemy(x, y):
                    enemy_position = {'x': x, 'y': y}
                    return enemy_position

        return enemy_position

    # Help Enemy move to Hero

    def _move_enemy_towards_hero(self, enemy_x, enemy_y):                       # TODO: Implement + Test
        pass

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


def main():
    h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

    w = Weapon(name="The Axe of Destiny", damage=20)
    h.equip(w)

    s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
    h.equip(s)

    map = Dungeon("level1.txt")
    map.spawn(h)
    map.print_map()

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


if __name__ == '__main__':
    # main()
    obj = Dungeon('level1.txt')
    obj.print_map()