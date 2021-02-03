class MissionValue:

	def __init__(self, name, main, rotation_a, rotation_b, rotation_c, no_rotation):
		self.Name = name
		self.Main = main
		self.A = rotation_a
		self.B = rotation_b
		self.C = rotation_c
		self.No_rotation = no_rotation

	def get_value(self, rotation="A"):
		if self.No_rotation:
			return 3 * self.Main
		elif rotation == "A":
			return self.A * self.Main
		elif rotation == "B":
			return self.B * self.Main
		elif rotation == "C":
			return self.C * self.Main


class Mission:

	MISSION_TYPE = {
		"(Spy)": MissionValue('Spy', 20, 2, 2, 2, False),
		"(Assassination)": MissionValue('Assassination', 1, 1, 1, 1, True),
		"(Assassination) Extra": MissionValue('Assassination Extra', 1, 1, 1, 1, True),
		"(Assault)": MissionValue('Assault', 20, 1, 1, 1, True),
		"(Capture)": MissionValue('Capture', 50, 1, 1, 1, True),
		"(Defection)": MissionValue('Defection', 1, 1, 1, 1, False),
		"(Defense)": MissionValue('Defense', 35, 5, 2, 1, False),
		"(Disruption)": MissionValue('Disruption', 40, 5, 2, 1, False),
		"(Excavation)": MissionValue('Excavation', 35, 5, 2, 1, False),
		"(Exterminate)": MissionValue('Exterminate', 30, 1, 1, 1, True),
		"(Free_Roam)": MissionValue('Free_Roam', 20, 1, 1, 1, True),
		"(Infested Salvage)": MissionValue('Infested Salvage', 1, 1, 1, 1, False),
		"(Interception)": MissionValue('Interception', 30, 5, 3, 1, False),
		"(Junction)": MissionValue('Junction', 1, 1, 1, 1, True),
		"(Mobile Defense)": MissionValue('Mobile Defense', 10, 5, 2, 1, False),
		"(Pursuit)": MissionValue('Pursuit', 35, 1, 1, 1, True),
		"(Rescue)": MissionValue('Rescue', 35, 1, 1, 1, False),
		"(Rush)": MissionValue('Rush', 35, 1, 1, 1, True),
		"(Sabotage)": MissionValue('Sabotage', 30, 1, 1, 1, True),
		"(Sanctuary Onslaught)": MissionValue('Sanctuary Onslaught', 20, 5, 2, 1, False),
		"(Skirmish)": MissionValue('Skirmish', 1, 1, 1, 1, True),
		"(Survival)": MissionValue('Survival', 20, 5, 2, 1, False),
		"(Caches)": MissionValue('Caches', 20, 5, 2, 1, False),
		"(Conclave)": MissionValue('Conclave', 1, 1, 1, 1, False),
		"(Conclave) Extra": MissionValue('Conclave Extra', 1, 1, 1, 1, False),
		"(Variant) Team Annihilation (Conclave)": MissionValue('Conclave Team Annihilation Variant', 1, 1, 1, 1, False),
		"(Variant) Cephalon Capture (Conclave)": MissionValue('Conclave Cephalon Capture Variant', 1, 1, 1, 1, False),
		"(Variant) Cephalon Capture (Conclave) Extra": MissionValue('Conclave Cephalon Capture Variant Extra', 1, 1, 1, 1, False),
		"(Variant) Team Annihilation (Conclave) Extra": MissionValue('Conclave Team Annihilation Variant Extra', 1, 1, 1, 1, False),
		"(Variant) Annihilation (Conclave)": MissionValue('Conclave Annihilation Variant', 1, 1, 1, 1, False),
		"(Variant) Annihilation (Conclave) Extra": MissionValue('Conclave Annihilation Variant Extra', 1, 1, 1, 1, False),
		"(Arena)": MissionValue('Arena', 1, 1, 1, 1, False),
		"(Low Risk) (Arena)": MissionValue('Arena Low Risk', 1, 1, 1, 1, False),
		"(Medium Risk) (Arena)": MissionValue('Arena Medium Risk', 1, 1, 1, 1, False),
		"(High Risk) (Arena)": MissionValue('Arena High Risk', 1, 1, 1, 1, False)
	}

	ROTATION_LIST = [
		"Rotation A",
		"Rotation B",
		"Rotation C"
	]

	def __init__(self, name, mission_type):
		#  print("new mission {} - {}\n".format(name, mission_type))
		self.Name = name
		self.Type = Mission.MISSION_TYPE[mission_type]
		self.Rotation_A = []
		self.Rotation_B = []
		self.Rotation_C = []
		self.Rotation_dic = {
			Mission.ROTATION_LIST[0]: self.Rotation_A,
			Mission.ROTATION_LIST[1]: self.Rotation_B,
			Mission.ROTATION_LIST[2]: self.Rotation_C
		}

	def add_loot(self, loot, luck, rotation=ROTATION_LIST[0]):
		#  print("add loot {} - {} - {}".format(loot, luck, rotation))
		if self.Type.No_rotation:
			self.Rotation_A.append({'loot': loot, 'luck': luck})
		else:
			self.Rotation_dic[rotation].append({'loot': loot, 'luck': luck})
