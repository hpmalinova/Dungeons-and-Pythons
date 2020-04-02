# test_hero.py

import unittest
from hero import Hero
from weapon import Weapon
from spell import Spell

class TestHeroValidation(unittest.TestCase):
    def test_hero_validation_raises_typeerror_if_name_not_str(self):
        name = ['Bron']
        title = 'Dragonslayer'
        health = 100
        mana = 100
        mana_regeneration_rate = 2
        exc = None

        try:
            Hero.validate_input_hero(name, title, health, mana, mana_regeneration_rate)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Name must be of "str" type.')

    def test_hero_validation_raises_typeerror_if_title_not_str(self):
        name = 'Bron'
        title = ['Dragonslayer']
        health = 100
        mana = 100
        mana_regeneration_rate = 2
        exc = None

        try:
            Hero.validate_input_hero(name, title, health, mana, mana_regeneration_rate)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Title must be of "str" type.')

    def test_hero_validation_raises_typeerror_if_mana_regen_rate_not_int(self):
        name = 'Bron'
        title = 'Dragonslayer'
        health = 100
        mana = 100
        mana_regeneration_rate = 'p'
        exc = None

        try:
            Hero.validate_input_hero(name, title, health, mana, mana_regeneration_rate)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Mana regeneration rate must be of "int" type.')

    def test_hero_validation_raises_exception_if_mana_regen_rate_negative(self):
        name = 'Bron'
        title = 'Dragonslayer'
        health = 100
        mana = 100
        mana_regeneration_rate = -5
        exc = None

        try:
            Hero.validate_input_hero(name, title, health, mana, mana_regeneration_rate)
        except Exception as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Mana regeneration rate cannot be negative.')

class TestHeroInit(unittest.TestCase):
    def test_hero_init_initializes_object_as_expected(self):
        name = 'Bron'
        title = 'Dragonslayer'
        health = 100
        mana = 100
        mana_regeneration_rate = 2
        exc = None

        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        self.assertEqual(getattr(test_obj, 'health'), 100)
        self.assertEqual(getattr(test_obj, 'max_health'), 100)
        self.assertEqual(getattr(test_obj, 'mana'), 100)
        self.assertEqual(getattr(test_obj, 'max_mana'), 100)
        self.assertEqual(getattr(test_obj, 'name'), 'Bron')
        self.assertEqual(getattr(test_obj, 'title'), 'Dragonslayer')
        self.assertEqual(getattr(test_obj, 'mana_regeneration_rate'), 2)

class TestHeroKnownAs(unittest.TestCase):
    def test_hero_known_as_represents_hero_as_expected(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        self.assertEqual(test_obj.known_as(), 'Bron the Dragonslayer')

class TestHeroAttack(unittest.TestCase):
    def test_hero_attack_raises_typeerror_if_means_are_not_of_str_type(self):
        exc = None

        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        
        try:
            test_obj.attack(by = ['testing'])
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Means of attack must be specified.')

    def test_hero_attack_raises_typeerror_if_means_are_no_argument_given(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        
        try:
            test_obj.attack()
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Means of attack must be specified.')

    def test_hero_attack_returns_zero_if_no_weapon_and_argument_is_weapon(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
  
        self.assertEqual(test_obj.attack(by = 'weapon'), 0)

    def test_hero_attack_returns_weapon_damage_if_equipped_weapon_and_argument_is_weapon(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        test_weapon = Weapon(name="The Axe of Destiny", damage=20)

        test_obj.equip(test_weapon)
  
        self.assertEqual(test_obj.attack(by = 'weapon'), 20)

    def test_hero_attack_returns_zero_if_no_spell_and_argument_is_magic(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
  
        self.assertEqual(test_obj.attack(by = 'magic'), 0)

    def test_hero_attack_returns_spell_damage_if_equipped_spell_and_argument_is_magic(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        test_spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

        test_obj.learn(test_spell)
  
        self.assertEqual(test_obj.attack(by = 'magic'), 30)

    def test_hero_attack_returns_zero_if_equipped_spell_but_mana_cost_greater_than_human_mana(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=20, mana_regeneration_rate=2)

        test_spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

        test_obj.learn(test_spell)
  
        self.assertEqual(test_obj.attack(by = 'magic'), 0)

    def test_hero_attack_raises_exception_if_unrecognized_attack(self):
        exc = None

        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=20, mana_regeneration_rate=2)

        try:
            test_obj.attack(by = 'testing')
        except Exception as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Unrecognized means of attack.')

class TestHeroTakeMana(unittest.TestCase):
    def test_hero_take_mana_method_cannot_give_more_mana_than_max(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        max_mana = 100
        mana_points = 200

        setattr(test_obj,'mana', 25)

        test_obj.take_mana(mana_points)

        self.assertEqual(getattr(test_obj,'mana'), max_mana)

    def test_hero_take_mana_method_gives_mana_equal_to_mana_points(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        max_mana = 100
        mana_points = 50
        expected_result = 75
        
        setattr(test_obj,'mana', 25)

        test_obj.take_mana(mana_points)

        self.assertEqual(getattr(test_obj,'mana'), expected_result)

if __name__ == '__main__':
    unittest.main()