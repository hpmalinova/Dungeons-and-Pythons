# test_dungeon.py

import unittest
from dungeon import Dungeon
from hero import Hero

class TestDungeonValidation(unittest.TestCase):
    def test_dungeon_validation_raises_typeerror_if_filename_not_str(self):
        test_filename = ['test']
        exc = None

        try:
            Dungeon.validate_input_dungeon(test_filename)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Filename must be of "str" type.')

class TestDungeonInit(unittest.TestCase):
    def test_dungeon_init_initializse_object_as_expected(self):
        test_filename = 'level1.txt'

        expected_result = [ ['S','.','#','#','.','.','.','.','.','T'],
                            ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                            ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                            ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                            ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G'] ] 

        test_obj = Dungeon(test_filename)
 
        self.assertEqual(getattr(test_obj,'map'), expected_result)

class TestDungeonSpawn(unittest.TestCase):
    def test_dungeon_spawn_raises_typeerror_if_argument_is_not_of_hero_type(self):
        test_hero = ['Test']
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
        exc = None

        try:
            test_obj.spawn(test_hero)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Argument must be of "Hero" type.')

    def test_dungeon_spawn_raises_exception_if_hero_already_in_dungeon(self):
        test_hero1 = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        test_hero2 = Hero(name="Jon", title="King in the North", health=100, mana=100, mana_regeneration_rate=2)
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)
        exc = None

        test_obj.spawn(test_hero1)

        try:
            test_obj.spawn(test_hero2)
        except Exception as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Cannot have more than 1 hero in the dungeon.')

    def test_dungeon_spawn_places_hero_on_the_map_and_initializes_hero_variable_with_argument(self):
        test_hero1 = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        test_filename = 'level1.txt'
        test_obj = Dungeon(test_filename)

        expected_result = [ ['H','.','#','#','.','.','.','.','.','T'],
                            ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                            ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                            ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                            ['#', '#', '#', 'T', '#', '#', '#', '#', '#', 'G'] ] 

        test_obj.spawn(test_hero1)

        self.assertEqual(getattr(test_obj, 'hero'), test_hero1)
        self.assertEqual(getattr(test_obj, 'map'), expected_result)

if __name__ == '__main__':
    unittest.main()