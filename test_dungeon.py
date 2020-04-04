# test_dungeon.py

import unittest

from dungeon import Dungeon
from hero import Hero
from enemy import Enemy
from weapon import Weapon
from spell import Spell
from armor import Armor
from potion import Potion


class TestDungeonValidation(unittest.TestCase):
    def test_dungeon_validation_raises_typeerror_if_filename_not_str(self):
        test_filename = ['test']

        with self.assertRaisesRegex(TypeError, 'Filename must be of "str" type.'):
            Dungeon.validate_input_dungeon(test_filename)


class TestDungeonInit(unittest.TestCase):
    def test_dungeon_init(self):
        test_filename = 'level1.txt'
        expected_result = [['S', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
                           ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                           ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                           ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                           ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G']]

        dungeon = Dungeon(test_filename)
        self.assertEqual(getattr(dungeon, 'map'), expected_result)

    def test_treasures_init(self):
        test_filename = 'level1.txt'
        dungeon = Dungeon(test_filename)
        expected_result = [Potion('mana', 40), Weapon('sword', 20), Armor('vest', 40),
                           Spell('Fireball', 40, 20, 6)]

        self.assertEqual(getattr(dungeon, 'treasures'), expected_result)


class TestDungeonSpawn(unittest.TestCase):
    def test_dungeon_spawn_raises_typeerror_if_argument_is_not_of_hero_type(self):
        test_hero = ['Test']
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        with self.assertRaisesRegex(TypeError, 'Argument must be of "Hero" type.'):
            test_obj.spawn(test_hero)

    def test_dungeon_spawn_raises_exception_if_hero_already_in_dungeon(self):
        test_hero1 = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        test_hero2 = Hero(name="Jon", title="King in the North", health=100, mana=100, mana_regeneration_rate=2)
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        test_obj.spawn(test_hero1)

        with self.assertRaisesRegex(AssertionError, 'Cannot have more than 1 hero in the dungeon.'):
            test_obj.spawn(test_hero2)

    def test_dungeon_spawn_places_hero_on_the_map_and_initializes_hero_variable_with_argument(self):
        test_hero1 = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        expected_result = [['H', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
                           ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                           ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                           ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                           ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G']]

        test_obj.spawn(test_hero1)

        self.assertEqual(getattr(test_obj, 'hero'), test_hero1)
        self.assertEqual(getattr(test_obj, 'map'), expected_result)

class TestDungeonCheckIfInvalidPosition(unittest.TestCase):
    def test_dungeon_check_if_invalid_position_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_invalid_position(-1, 5), True)
        self.assertEqual(test_obj._check_if_invalid_position(0, 1), False)

class TestDungeonCheckIfObstacle(unittest.TestCase):
    def test_dungeon_check_if_obstacle_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_obstacle(0, 2), True)
        self.assertEqual(test_obj._check_if_obstacle(0, 1), False)

class TestDungeonCheckIfWalkablePath(unittest.TestCase):
    def test_dungeon_check_if_walkable_path_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_walkable_path(0, 1), True)
        self.assertEqual(test_obj._check_if_walkable_path(0, 9), False) 

class TestDungeonCheckIfWalkablePath(unittest.TestCase):
    def test_dungeon_check_if_walkable_path_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_walkable_path(0, 1), True)
        self.assertEqual(test_obj._check_if_walkable_path(0, 9), False) 

class TestDungeonCheckIfTreasure(unittest.TestCase):
    def test_dungeon_check_if_treasure_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_treasure(0, 9), True)
        self.assertEqual(test_obj._check_if_treasure(2, 5), False)

class TestDungeonCheckIfEnemy(unittest.TestCase):
    def test_dungeon_check_if_enemy_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_enemy(2, 5), True)
        self.assertEqual(test_obj._check_if_enemy(0, 1), False)

class TestDungeonCheckIfSpawnPoint(unittest.TestCase):
    def test_dungeon_check_if_spawn_point_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_spawn_point(0, 0), True)
        self.assertEqual(test_obj._check_if_spawn_point(0, 1), False)

class TestDungeonCheckIfGetaway(unittest.TestCase):
    def test_dungeon_check_if_getaway_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
     
        self.assertEqual(test_obj._check_if_gateway(4, 9), True)
        self.assertEqual(test_obj._check_if_gateway(0, 1), False)

class TestDungeonMoveHeroToPosition(unittest.TestCase):
    def test_dungeon_move_hero_to_position_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
        test_hero1 = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        test_obj.spawn(test_hero1)

        expected_result = [ ['.','H','#','#','.','.','.','.','.','T'],
                            ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                            ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                            ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                            ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G'] ]

        test_obj._Dungeon__move_hero_to_position(0, 1, '.')

        self.assertEqual(getattr(test_obj, 'map'), expected_result)

if __name__ == '__main__':
    unittest.main()
