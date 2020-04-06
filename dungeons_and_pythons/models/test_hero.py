# test_hero.py

import unittest
from dungeons_and_pythons.models import Hero
from dungeons_and_pythons.models import Weapon
from dungeons_and_pythons.models import Spell
from dungeons_and_pythons.models import Potion


class TestHeroValidation(unittest.TestCase):
    def test_hero_validation_raises_typeerror_if_name_not_str(self):
        name = ['Bron']
        title = 'Dragonslayer'
        mana_regeneration_rate = 2

        with self.assertRaisesRegex(TypeError, 'Name must be of "str" type.'):
            Hero.validate_input_hero(name, title, mana_regeneration_rate)

    def test_hero_validation_raises_typeerror_if_title_not_str(self):
        name = 'Bron'
        title = ['Dragonslayer']
        mana_regeneration_rate = 2

        with self.assertRaisesRegex(TypeError, 'Title must be of "str" type.'):
            Hero.validate_input_hero(name, title, mana_regeneration_rate)

    def test_hero_validation_raises_typeerror_if_mana_regen_rate_not_int(self):
        name = 'Bron'
        title = 'Dragonslayer'
        mana_regeneration_rate = 'p'

        with self.assertRaisesRegex(TypeError, 'Mana regeneration rate must be of "int" type.'):
            Hero.validate_input_hero(name, title, mana_regeneration_rate)

    def test_hero_validation_raises_exception_if_mana_regen_rate_negative(self):
        name = 'Bron'
        title = 'Dragonslayer'
        mana_regeneration_rate = -5

        with self.assertRaisesRegex(ValueError, 'Mana regeneration rate cannot be negative.'):
            Hero.validate_input_hero(name, title, mana_regeneration_rate)


class TestHeroInit(unittest.TestCase):
    def test_hero_init_initializes_object_as_expected(self):
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


class TestHeroTakeMana(unittest.TestCase):
    def test_hero_take_mana_method_cannot_give_more_mana_than_max(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        max_mana = 100
        mana_points = 200

        setattr(test_obj, 'mana', 25)

        test_obj.take_mana(mana_points)

        self.assertEqual(getattr(test_obj, 'mana'), max_mana)

    def test_hero_take_mana_method_gives_mana_equal_to_mana_points(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        setattr(test_obj, 'mana', 25)

        test_obj.take_mana(50)

        self.assertEqual(getattr(test_obj, 'mana'), 75)


class TestHeroAttack(unittest.TestCase):
    def test_when_unrecognise_means_then_raises_value_error(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        with self.assertRaisesRegex(ValueError, 'Unrecognized means of attack.'):
            test_obj.attack(by='testing')

    def test_when_hero_has_no_weapons_then_return_none(self):
        test_obj = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        self.assertEqual(test_obj.attack(by='weapon'), None)
        self.assertEqual(test_obj.attack(by='magic'), None)
        self.assertEqual(test_obj.attack(), None)

    def test_when_hero_wants_to_attack_with_weapon_and_has_it_then_return_weapon(self):
        hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        weapon = Weapon(name="The Axe of Destiny", damage=20)

        weapon.equip_to(hero)

        self.assertEqual(hero.attack(by='weapon'), weapon)

    def test_when_hero_wants_to_attack_with_magic_and_has_and_can_cast_spell_then_return_spell(self):
        hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

        spell.equip_to(hero)

        self.assertEqual(hero.attack(by='magic'), spell)
        self.assertEqual(getattr(hero, 'mana'), 50)

    def test_when_hero_wants_to_attack_with_magic_and_has_it_but_has_no_mana_then_return_none(self):
        hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
        spell = Spell(name="Fireball", damage=30, mana_cost=150, cast_range=2)

        spell.equip_to(hero)

        self.assertEqual(hero.attack(by='magic'), None)


class TestDrinkManaPotion(unittest.TestCase):
    def test_drink_mana_potion(self):
        hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

        setattr(hero, 'mana', 20)

        # restore mana
        potion = Potion('mana', 20)
        potion.equip_to(hero)

        self.assertEqual(getattr(hero, 'mana'), 40)


if __name__ == '__main__':
    unittest.main()
