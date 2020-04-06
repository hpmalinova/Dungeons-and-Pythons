# test_human.py

import unittest
from dungeons_and_pythons.models import Human
from dungeons_and_pythons.models import Weapon
from dungeons_and_pythons.models import Spell
from dungeons_and_pythons.models import Armor
from dungeons_and_pythons.models import Potion


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

    def test_human_validate_input_raises_exception_if_health_is_negative(self):
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

        self.assertFalse(test_obj1.is_alive())
        self.assertTrue(test_obj2.is_alive())


class TestCanCast(unittest.TestCase):
    def test_can_cast_when_human_has_no_spell_then_return_false(self):
        human = Human(50, 50)

        self.assertFalse(human.can_cast())

    def test_can_cast_when_human_has_spell_but_no_mana_to_cast_then_return_false(self):
        human = Human(50, 50)
        spell = Spell('abrakadarba', 20, 70, 2)
        spell.equip_to(human)

        self.assertFalse(human.can_cast())

    def test_can_cast_when_human_has_spell_and_enough_mana_then_return_true(self):
        human = Human(50, 50)
        spell = Spell('abrakadarba', 20, 30, 2)
        spell.equip_to(human)

        self.assertTrue(human.can_cast())


class TestHumanTakeHealing(unittest.TestCase):
    def test_human_take_healing_method_cannot_heal_the_dead(self):
        test_health = 0
        test_mana = 55

        healing_points = 50

        test_obj = Human(test_health, test_mana)

        self.assertFalse(test_obj.take_healing(healing_points))

    def test_human_take_healing_method_cannot_heal_more_than_max_health(self):
        max_health = 50

        test_obj = Human(50, 50)

        setattr(test_obj, 'health', 25)

        test_obj.take_healing(50)

        self.assertEqual(getattr(test_obj, 'health'), max_health)

    def test_human_take_healing_method_heals_with_amount_of_healing_points(self):
        max_health = 100
        test_obj = Human(max_health, 5)

        setattr(test_obj, 'health', 25)

        test_obj.take_healing(50)

        self.assertEqual(getattr(test_obj, 'health'), 75)


class TestHumanTakeDamageWithNoArmor(unittest.TestCase):
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


class TestHumanTakeDamageWithArmor(unittest.TestCase):
    def test_when_human_has_less_armor_than_the_damage_taken_then_take_damage(self):
        human = Human(health=100, mana=100)
        armor = Armor(name="Dragon Armor", armor_points=10)
        armor.equip_to(human)

        human.take_damage(50)

        self.assertEqual(getattr(human, 'health'), 60)
        self.assertEqual(getattr(human, 'armor'), armor)

    def test_when_human_has_more_armor_than_damage_taken_then_dont_take_damage(self):
        human = Human(health=100, mana=100)
        armor = Armor(name="Dragon Armor", armor_points=30)
        armor.equip_to(human)

        human.take_damage(20)

        self.assertEqual(getattr(human, 'health'), 100)
        self.assertEqual(getattr(human, 'armor'), armor)


class TestEquip(unittest.TestCase):
    def test_human_equip_raises_typeerror_if_item_is_not_equipable(self):
        human = Human(100, 100)

        with self.assertRaisesRegex(TypeError, 'Invalid item type.'):
            human.equip('testing')

    def test_when_human_has_no_equipable_item_then_equip_new_item(self):
        human = Human(100, 100)

        weapon = Weapon(name='The Axe of Destiny', damage=20)
        spell = Spell(name='Abrakadarba', damage=20, mana_cost=30, cast_range=2)
        armor = Armor(name='The protector', armor_points=5)

        weapon.equip_to(human)
        spell.equip_to(human)
        armor.equip_to(human)

        self.assertEqual(getattr(human, 'weapon'), weapon)
        self.assertEqual(getattr(human, 'spell'), spell)
        self.assertEqual(getattr(human, 'armor'), armor)

    def test_when_human_has_equipable_item_and_new_item_is_weaker_then_stay_with_old_item(self):
        human = Human(100, 100)
        weapon = Weapon(name='The Axe of Destiny', damage=20)
        weapon.equip_to(human)

        weapon2 = Weapon(name='The Axe of Destiny', damage=10)
        weapon2.equip_to(human)

        self.assertEqual(getattr(human, 'weapon'), weapon)

    def test_when_human_has_equipable_item_and_new_item_is_stronger_then_equip_new_item(self):
        human = Human(100, 100)
        weapon = Weapon(name='The Axe of Destiny', damage=20)
        weapon.equip_to(human)

        weapon2 = Weapon(name='The Axe of Destiny', damage=30)
        weapon2.equip_to(human)

        self.assertEqual(getattr(human, 'weapon'), weapon2)

    def test_when_human_has_health_potion_then_drink_it(self):
        max_health = 100
        human = Human(max_health, 100)
        health_potion = Potion(potion_type='health', points=20)
        setattr(human, 'health', 50)
        health_potion.equip_to(human)

        self.assertEqual(getattr(human, 'health'), 70)


class TestStrongestMean(unittest.TestCase):
    def test_when_weapon_is_stronger_than_spell_then_return_weapon(self):
        human = Human(100, 100)
        weapon = Weapon(name='The Axe of Destiny', damage=20)
        weapon.equip_to(human)

        spell = Spell(name='The Fireball of Destiny', damage=10, mana_cost=10, cast_range=2)
        spell.equip_to(human)

        self.assertEqual(human.get_strongest_mean(), weapon)

    def test_when_weapon_is_equal_to_spell_then_return_weapon(self):
        human = Human(100, 100)
        weapon = Weapon(name='The Axe of Destiny', damage=20)
        weapon.equip_to(human)

        spell = Spell(name='The Fireball of Destiny', damage=20, mana_cost=10, cast_range=2)
        spell.equip_to(human)

        self.assertEqual(human.get_strongest_mean(), weapon)

    def test_when_spell_is_stronger_than_weapon_but_has_no_mana_then_return_weapon(self):
        human = Human(100, 100)
        weapon = Weapon(name='The Axe of Destiny', damage=20)
        weapon.equip_to(human)

        spell = Spell(name='The Fireball of Destiny', damage=50, mana_cost=150, cast_range=2)
        spell.equip_to(human)

        self.assertEqual(human.get_strongest_mean(), weapon)

    def test_when_spell_is_stronger_than_weapon_and_has_mana_then_return_spell(self):
        human = Human(100, 100)
        weapon = Weapon(name='The Axe of Destiny', damage=20)
        weapon.equip_to(human)

        spell = Spell(name='The Fireball of Destiny', damage=50, mana_cost=10, cast_range=2)
        spell.equip_to(human)

        self.assertEqual(human.get_strongest_mean(), spell)

    def test_when_human_has_no_means_then_return_none(self):
        human = Human(100, 100)

        self.assertEqual(human.get_strongest_mean(), None)


if __name__ == '__main__':
    unittest.main()
