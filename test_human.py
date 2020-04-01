# test_human.py

import unittest
from human import Human

class TestHumanValidation(unittest.TestCase):
    def test_human_validate_input_raises_typeerror_if_health_is_not_int(self):
        test_health = 'p'
        test_mana = 50
        exc = None

        try:
            Human.validate_input(test_health, test_mana)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Health must be of "int" / "float" type.')

    def test_human_validate_input_raises_typeerror_if_mana_is_not_int(self):
        test_health = 100
        test_mana = 'p'
        exc = None

        try:
            Human.validate_input(test_health, test_mana)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Mana must be of "int" type.')


class TestHumanInit(unittest.TestCase):
    def test_human_init_initializes_object_as_expected(self):
        test_health = 100
        test_mana = 50

        test_obj = Human(test_health, test_mana)

        self.assertEqual(getattr(test_obj, 'health'), 100)
        self.assertEqual(getattr(test_obj, 'max_health'), 100)
        self.assertEqual(getattr(test_obj, 'mana'), 50)

class TestHumanIsAlive(unittest.TestCase):
    def test_human_is_alive_method_works_as_expected(self):
        test_health1 = 0
        test_mana1 = 50

        test_obj1 = Human(test_health1, test_mana1)

        test_health2 = 100
        test_mana2 = 50

        test_obj2 = Human(test_health2, test_mana2)

        self.assertEqual(test_obj1.is_alive(), False)
        self.assertEqual(test_obj2.is_alive(), True)

class TestHumanGetHealth(unittest.TestCase):
    def test_human_get_health_method_works_as_expected(self):
        test_health = 77
        test_mana = 50

        test_obj = Human(test_health, test_mana)

        self.assertEqual(test_obj.get_health(), 77)

class TestHumanGetMana(unittest.TestCase):
    def test_human_get_mana_method_works_as_expected(self):
        test_health = 100
        test_mana = 55

        test_obj = Human(test_health, test_mana)

        self.assertEqual(test_obj.get_mana(), 55)

class TestHumanTakeDamage(unittest.TestCase):
    def test_human_take_damage_method_raises_typeerror_if_damage_is_not_int_or_float(self):
        test_health = 100
        test_mana = 55
        test_obj = Human(test_health, test_mana)
        exc = None

        try:
            test_obj.take_damage('p')
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Damage must be of "int" / "float" type.')

    def test_human_take_damage_method_changes_health_to_zero_if_damage_greater_than_health(self):
        test_health = 50
        test_mana = 55
       
        test_obj = Human(test_health, test_mana)

        test_obj.take_damage(150)

        self.assertEqual(getattr(test_obj, 'health'), 0)

    def test_human_take_damage_method_works_as_expected_if_health_greater_than_damage(self):
        test_health = 50
        test_mana = 55
       
        test_obj = Human(test_health, test_mana)

        test_obj.take_damage(25)

        self.assertEqual(getattr(test_obj, 'health'), 25)

class TestHumanTakeHealing(unittest.TestCase):
    def test_human_take_healing_method_cannot_heal_the_dead(self):
        test_health = 0
        test_mana = 55

        healing_points = 50
       
        test_obj = Human(test_health, test_mana)

        self.assertEqual(test_obj.take_healing(healing_points), False)

    def test_human_take_healing_method_cannot_heal_more_than_max_health(self):
        test_health = 50
        test_mana = 55

        max_health = 50
        healing_points = 50
       
        test_obj = Human(test_health, test_mana)

        setattr(test_obj,'health', 25)

        test_obj.take_healing(healing_points)

        self.assertEqual(getattr(test_obj,'health'), max_health)

    def test_human_take_healing_method_heals_with_amount_of_healing_points(self):
        test_health = 100
        test_mana = 55

        healing_points = 50
       
        test_obj = Human(test_health, test_mana)

        setattr(test_obj, 'health', 25)

        test_obj.take_healing(healing_points)

        self.assertEqual(getattr(test_obj, 'health'), 75)

class TestHumanTakeMana(unittest.TestCase):
    def test_human_take_mana_method_cannot_give_more_mana_than_max(self):
        test_health = 50
        test_mana = 50

        max_mana = 50
        mana_points = 50
       
        test_obj = Human(test_health, test_mana)

        setattr(test_obj,'mana', 25)

        test_obj.take_mana(mana_points)

        self.assertEqual(getattr(test_obj,'mana'), max_mana)

    def test_human_take_mana_method_gives_mana_equal_to_mana_points(self):
        test_health = 100
        test_mana = 100

        mana_points = 50
       
        test_obj = Human(test_health, test_mana)

        setattr(test_obj, 'mana', 25)

        test_obj.take_mana(mana_points)

        self.assertEqual(getattr(test_obj, 'mana'), 75)

if __name__ == '__main__':
    unittest.main()