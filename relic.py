
class Relic:
	INTACT = 0
	EXCEPTIONAL = 1
	FLAWLESS = 2
	RADIANT = 3
	COMMON = 0
	UNCOMMON = 1
	RARE = 2

	RARITY_NAME = {
		"Rare (2.00%)": RARE,
		"Uncommon (11.00%)": UNCOMMON,
		"Uncommon (25.33%)": COMMON
	}

	def __init__(self, name):
		#  print("new relic {}".format(name))
		super().__init__()
		self.Name = name
		self.Common = []
		self.Uncommon = []
		self.Rare = []
		self.Vaulted = True

	def change_vaulted(self, statue):
		self.Vaulted = statue

	def add_level(self, rarity, loot):
		#  print("add", rarity, loot)
		if rarity == Relic.COMMON:
			self.Common.append(loot)
		elif rarity == Relic.UNCOMMON:
			self.Uncommon.append(loot)
		elif rarity == Relic.RARE:
			self.Rare.append(loot)

	@staticmethod
	def cost(level):
		if level == Relic.INTACT:
			return 0
		elif level == Relic.EXCEPTIONAL:
			return 25
		elif level == Relic.FLAWLESS:
			return 50
		else:
			return 100

	@staticmethod
	def luck_common(level, player_number):
		if level == Relic.INTACT:
			return 1 - ((1 - 0.2533) ** player_number)
		elif level == Relic.EXCEPTIONAL:
			return 1 - (0.2333 ** player_number)
		elif level == Relic.FLAWLESS:
			return 1 - (0.2 ** player_number)
		else:
			return 1 - (0.1667 ** player_number)

	@staticmethod
	def luck_uncommon(level, player_number):
		if level == Relic.INTACT:
			return 1 - (0.11 ** player_number)
		elif level == Relic.EXCEPTIONAL:
			return 1 - (0.13 ** player_number)
		elif level == Relic.FLAWLESS:
			return 1 - (0.17 ** player_number)
		else:
			return 1 - (0.2 ** player_number)

	@staticmethod
	def luck_rare(level, player_number):
		if level == Relic.INTACT:
			return 1 - (0.02 ** player_number)
		elif level == Relic.EXCEPTIONAL:
			return 1 - (0.04 ** player_number)
		elif level == Relic.FLAWLESS:
			return 1 - (0.06 ** player_number)
		else:
			return 1 - (0.1 ** player_number)
