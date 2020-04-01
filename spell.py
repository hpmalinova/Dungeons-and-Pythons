class Spell:
	def __init__(self, name, damage, mana_cost, cast_range):
		self.name = name
		
		assert damage >= 0, 'Damage dealt can`t be a negative number.'
		self.damage = damage

		assert mana_cost >= 0, 'Mana cost can`t be a negative number.'
		self.mana_cost = mana_cost

		assert cast_range >= 0, 'Cast range can`t be a negative number.'
		self.cast_range = cast_range