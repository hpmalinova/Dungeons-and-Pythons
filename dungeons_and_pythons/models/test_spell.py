import unittest
from dungeons_and_pythons.models import Spell

class TestSpell(unittest.TestCase):
	def test_when_damage_is_negative_number_then_raise_error(self):
		with self.assertRaisesRegex(AssertionError, 'Damage dealt can`t be a negative number.'):
			spell = Spell('Fireball', -30, 5, 6)
    	
	def test_when_mana_cost_is_negative_number_then_raise_error(self):
		with self.assertRaisesRegex(AssertionError, 'Mana cost can`t be a negative number.'):
			spell = Spell('Fireball', 30, -5, 6)

	def test_when_cast_range_is_negative_number_then_raise_errors(self):
		with self.assertRaisesRegex(AssertionError, 'Cast range can`t be a negative number.'):
			spell = Spell('Fireball', 30, 5, -6)			

if __name__ == '__main__':
	unittest.main()		
