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

        self.assertTrue(test_obj._check_if_invalid_position(-1, 5))
        self.assertFalse(test_obj._check_if_invalid_position(0, 1))


class TestDungeonCheckIfObstacle(unittest.TestCase):
    def test_dungeon_check_if_obstacle_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        self.assertTrue(test_obj._check_if_obstacle(0, 2))
        self.assertFalse(test_obj._check_if_obstacle(0, 1))


class TestDungeonCheckIfWalkablePath(unittest.TestCase):
    def test_dungeon_check_if_walkable_path_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        self.assertTrue(test_obj._check_if_walkable_path(0, 1))
        self.assertFalse(test_obj._check_if_walkable_path(0, 9))


class TestDungeonCheckIfTreasure(unittest.TestCase):
    def test_dungeon_check_if_treasure_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        self.assertTrue(test_obj._check_if_treasure(0, 9))
        self.assertFalse(test_obj._check_if_treasure(2, 5))


class TestDungeonCheckIfEnemy(unittest.TestCase):
    def test_dungeon_check_if_enemy_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        self.assertTrue(test_obj._check_if_enemy(2, 5))
        self.assertFalse(test_obj._check_if_enemy(0, 1))


class TestDungeonCheckIfSpawnPoint(unittest.TestCase):
    def test_dungeon_check_if_spawn_point_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        self.assertTrue(test_obj._check_if_spawn_point(0, 0))
        self.assertFalse(test_obj._check_if_spawn_point(0, 1))


class TestDungeonCheckIfGetaway(unittest.TestCase):
    def test_dungeon_check_if_getaway_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        self.assertTrue(test_obj._check_if_gateway(4, 9))
        self.assertFalse(test_obj._check_if_gateway(0, 1))


class TestDungeonMoveHeroToPosition(unittest.TestCase):
    def test_dungeon_move_hero_to_position_works_as_expected(self):
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
        test_hero1 = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        test_obj.spawn(test_hero1)

        expected_result = [['.', 'H', '#', '#', '.', '.', '.', '.', '.', 'T'],
                           ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                           ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                           ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                           ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G']]

        test_obj._Dungeon__move_hero_to_position(0, 1, '.')

        self.assertEqual(getattr(test_obj, 'map'), expected_result)


class TestCheckForEnemy(unittest.TestCase):
    def test_check_for_enemy_when_no_enemy_in_range_then_return_invalid_enemy_position(self):
        dungeon = Dungeon('level1.txt')
        hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        dungeon.spawn(hero)

        expected_enemy_position = {'x': -1, 'y': -1}
        # dungeon_map = [['H', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
        #                ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
        #                ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
        #                ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
        #                ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G']]

        self.assertEqual(dungeon.check_for_enemy(2), expected_enemy_position)

    def test_check_for_enemy_when_enemy_in_range_1_then_return_invalid_enemy_position(self):
        dungeon = Dungeon('level1.txt')
        hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        dungeon.spawn(hero)
        dungeon.move_hero('right')
        dungeon.move_hero('down')
        dungeon.move_hero('down')
        dungeon.move_hero('down')
        #print(dungeon.hero_coordinates) x:3, y:1

        expected_enemy_position = {'x': 3, 'y': 2}
        # dungeon_map = [['.', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
        #                ['#', '.', '#', '#', '.', '.', '#', '#', '#', '.'],
        #                ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
        #                ['#', 'H', 'E', '.', '.', '.', '#', '#', '#', '.'],
        #                ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G']]

        self.assertEqual(dungeon.check_for_enemy(1), expected_enemy_position)


if __name__ == '__main__':
    unittest.main()
