# test_enemy.py

import unittest
from dungeons_and_pythons.models import Enemy
from dungeons_and_pythons.models import Weapon
from dungeons_and_pythons.models import Spell


class TestEnemyValidation(unittest.TestCase):
    def test_enemy_validation_raises_typeerror_if_damage_not_int_or_float(self):
        damage = 'damage'

        with self.assertRaisesRegex(TypeError, 'Damage must be of "int" / "float" type.'):
            Enemy.validate_input_enemy(damage)

    def test_enemy_validation_raises_exception_if_damage_is_negative(self):
        damage = -5

        with self.assertRaisesRegex(ValueError, 'Damage should be positive.'):
            Enemy.validate_input_enemy(damage)


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
        enemy = Enemy(100, 50, 20)

        self.assertFalse(enemy.take_mana())


class TestEnemyAttack(unittest.TestCase):
    def test_when_enemy_has_no_weapons_or_spells_then_return_fists(self):
        test_obj = Enemy(150, 50, 20)

        self.assertEqual(test_obj.attack(), Weapon('Fists', 20))

    def test_when_enemy_fists_are_stronger_than_weapons_then_return_fists(self):
        enemy = Enemy(150, 50, 50)
        weapon = Weapon('Axe', 10)
        weapon.equip_to(enemy)

        self.assertEqual(enemy.attack(), Weapon('Fists', 50))

    def test_when_enemy_fists_are_weaker_than_weapon_then_return_weapon(self):
        enemy = Enemy(150, 50, 50)
        weapon = Weapon('Axe', 100)
        weapon.equip_to(enemy)

        self.assertEqual(enemy.attack(), weapon)

    def test_when_enemy_fists_are_weaker_than_spell_then_return_spell(self):
        enemy = Enemy(150, 50, 50)
        spell = Spell(name="Fireball", damage=150, mana_cost=50, cast_range=2)

        spell.equip_to(enemy)

        self.assertEqual(enemy.attack(), spell)
        self.assertEqual(getattr(enemy, 'mana'), 0)


if __name__ == '__main__':
    unittest.main()
