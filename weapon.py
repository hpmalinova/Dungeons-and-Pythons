from treasure import Treasure

class Weapon(Treasure):
	def __init__(self, name, damage):
		self.name = name
		assert damage >= 0, 'Damage of weapon can`t be a negative number' 
		self.damage = damage

	def equip_to(self, human):
		human.equip(self, weapon=self)

	def __eq__(self, other):
		return self.name == other.name and self.damage == other.damage

	def __lt__(self, other):
		return self.damage < other.damage		