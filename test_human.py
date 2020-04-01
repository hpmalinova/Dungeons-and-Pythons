# test_human.py

import unittest
from human import Human
from weapon import Weapon
from spell import Spell

class TestHumanValidation(unittest.TestCase):
    def test_human_validate_input_raises_typeerror_if_health_is_not_int(self):
        test_health = 'p'
        test_mana = 50
        exc = None

        try:
            Human.validate_input_human(test_health, test_mana)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Health must be of "int" / "float" type.')

    def test_human_validate_input_raises_typeerror_if_mana_is_not_int(self):
        test_health = 100
        test_mana = 'p'
        exc = None

        try:
            Human.validate_input_human(test_health, test_mana)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Mana must be of "int" type.')

    def test_human_validate_input_raises_exception_if_mana_is_negative(self):
        test_health = 100
        test_mana = -5
        exc = None

        try:
            Human.validate_input_human(test_health, test_mana)
        except Exception as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Mana cannot be less than 0.')

    def test_human_validate_input_raises_exception_if_mana_is_negative(self):
        test_health = -5
        test_mana = 100
        exc = None

        try:
            Human.validate_input_human(test_health, test_mana)
        except Exception as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Health cannot be less than 0.')

    def test_human_validate_input_passes_with_zero_mana(self):
        test_health = 100
        test_mana = 0

        Human.validate_input_human(test_health, test_mana)
        
    def test_human_validate_input_passes_with_zero_health(self):
        test_health = 0
        test_mana = 50

        Human.validate_input_human(test_health, test_mana)

class TestHumanInit(unittest.TestCase):
    def test_human_init_initializes_object_as_expected(self):
        test_health = 100
        test_mana = 50

        test_obj = Human(test_health, test_mana)

        self.assertEqual(getattr(test_obj, 'health'), 100)
        self.assertEqual(getattr(test_obj, 'max_health'), 100)
        self.assertEqual(getattr(test_obj, 'mana'), 50)
        self.assertEqual(getattr(test_obj, 'max_mana'), 50)
        self.assertEqual(getattr(test_obj, 'weapon'), None)
        self.assertEqual(getattr(test_obj, 'spell'), None)

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

class TestHumanEquip(unittest.TestCase):
    def test_human_equip_raises_typeerror_if_arg_is_not_weapon(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)
        exc = None

        test_weapon = ['testing']

        try:
            test_obj.equip(test_weapon)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Argument must be of "Weapon" type.')

    def test_human_equip_initializes_object_with_weapon(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)

        test_weapon = Weapon(name="The Axe of Destiny", damage=20)

        test_obj.equip(test_weapon)

        self.assertEqual(getattr(test_obj, 'weapon'), test_weapon)

class TestHumanLearn(unittest.TestCase):
    def test_human_learn_raises_typeerror_if_arg_is_not_spell(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)
        exc = None

        test_spell = ['testing']

        try:
            test_obj.learn(test_spell)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Argument must be of "Spell" type.')

    def test_human_learn_initializes_object_with_spell(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)

        test_spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

        test_obj.learn(test_spell)

        self.assertEqual(getattr(test_obj, 'spell'), test_spell)

class TestHumanCanCast(unittest.TestCase):
    def test_human_can_cast_returns_false_if_no_spell_learned(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)

        self.assertEqual(test_obj.can_cast(), False)

    def test_human_can_cast_returns_true_if_human_has_enough_mana_to_cast_spell(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)

        test_spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

        test_obj.learn(test_spell)

        self.assertEqual(test_obj.can_cast(), True)

    def test_human_can_cast_returns_false_if_human_has_got_enough_mana_to_cast_spell(self):
        test_health = 100
        test_mana = 100
        test_obj = Human(test_health, test_mana)

        test_spell = Spell(name="Fireball", damage=30, mana_cost=150, cast_range=2)

        test_obj.learn(test_spell)

        self.assertEqual(test_obj.can_cast(), False)

if __name__ == '__main__':
    unittest.main()