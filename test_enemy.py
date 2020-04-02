# test_enemy.py

import unittest
from enemy import Enemy
from weapon import Weapon
from spell import Spell

class TestEnemyValidation(unittest.TestCase):
    def test_enemy_validation_raises_typeerror_if_damage_not_int_or_float(self):
        damage = 'damage'
        exc = None

        try:
            Enemy.validate_input_enemy(damage)
        except TypeError as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Damage must be of "int" / "float" type.')

    def test_enemy_validation_raises_exception_if_damage_is_negative(self):
        damage = -5
        exc = None

        try:
            Enemy.validate_input_enemy(damage)
        except Exception as err:
            exc = err

        self.assertIsNotNone(exc)
        self.assertEqual(str(exc), 'Damage cannot be negative.')

class TestEnemyInit(unittest.TestCase):
    def test_enemy_init_initializes_object_as_expected(self):
        health = 100
        mana = 50
        damage = 20

        test_obj = Enemy(health, mana, damage)

        self.assertEqual(getattr(test_obj, 'health'), health)
        self.assertEqual(getattr(test_obj, 'mana'), mana)
        self.assertEqual(getattr(test_obj, 'damage'), damage)

class TestEnemyTakeMana(unittest.TestCase):
    def test_enemy_take_mana_returns_false(self):
        health = 100
        mana = 50
        damage = 20

        test_obj = Enemy(health, mana, damage)

        self.assertEqual(test_obj.take_mana(), False)

class TestEnemyAttack(unittest.TestCase):
    def test_enemy_attack_uses_starting_damage_if_no_weapons_or_spells(self):
        health = 100
        mana = 50
        damage = 20

        test_obj = Enemy(health, mana, damage)

        self.assertEqual(test_obj.attack(), 20)

    def test_enemy_attack_uses_max_damage_from_weapon_spell_starting(self):
        health = 100
        mana = 50
        damage = 20

        test_obj = Enemy(health, mana, damage)       
        
        test_weapon = Weapon(name="The Axe of Destiny", damage=40)
        test_spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2) 

        test_obj.equip(test_weapon)
        test_obj.learn(test_spell)

        self.assertEqual(test_obj.attack(), 40)

    def test_enemy_attack_reduces_mana_by_mana_cost_if_spell_has_most_damage(self):
        health = 100
        mana = 50
        damage = 20

        test_obj = Enemy(health, mana, damage)       
        
        test_weapon = Weapon(name="The Axe of Destiny", damage=40)
        test_spell = Spell(name="Fireball", damage=50, mana_cost=50, cast_range=2) 

        test_obj.equip(test_weapon)
        test_obj.learn(test_spell)

        self.assertEqual(test_obj.attack(), 50)
        self.assertEqual(getattr(test_obj,'mana'), 0)



if __name__ == '__main__':
    unittest.main()