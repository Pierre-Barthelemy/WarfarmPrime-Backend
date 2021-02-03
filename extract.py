import requests
from html.parser import HTMLParser
from relic import Relic
from mission import Mission


class MyHTMLParser(HTMLParser):

	TABLE_LIST = [
		"Missions", "Relics", "Keys", "Dynamic Location Rewards", "Sorties", "Cetus Bounty Rewards",
		"Orb Vallis Bounty Rewards", "Mod Drops by Source", "Mod Drops by Mod",
		"Blueprint/Part Drops by Source", "Blueprint/Part Drops by Item", "Resource Drops by Source",
		"Sigil Drops by Source", "Additional Item Drops by Source"
	]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.Missions = []
		self.Relics = []
		self.Table_number = 0
		self.Table_open = False

		self.Title = False
		self.Rotation = False

		self.Title_Text = ""
		self.Rotation_Number = ""

		self.Ignore = False
		self.Loot = ""
		self.Loot_Rarity = ""

	def mark_vaulted(self):
		for mission in self.Missions:
			for loot in mission.Rotation_A:
				for relic in self.Relics:
					if relic.Name == loot['loot']:
						relic.change_vaulted(False)

	def error(self, message):
		pass

	@staticmethod
	def parse_luck(text):
		position = text.find('(')
		return float(text[position+1:-2]) / 100

	def handle_starttag(self, tag, attrs):
		if len(attrs) > 0 and attrs[0][1] == "blank-row":
			self.Title = False
			self.Title_Text = ""
			self.Rotation = False
			self.Rotation_Number = None
		if tag == "table":
			self.Table_number += 1
			self.Table_open = True
			self.Title = True
			self.Title_Text = ""
			self.Rotation = False
			self.Rotation_Number = None
			self.Loot = ""
			self.Loot_Rarity = ""
		if tag == "th":
			if self.Title_Text == "":
				self.Title = True
			else:
				self.Rotation = True

	def handle_endtag(self, tag):
		if tag == "table":
			self.Table_open = False
		if tag == "th":
			self.Title = False

	def handle_mission(self, data):
		if self.Title:
			self.Title_Text = data
			self.Title = False
			position = self.Title_Text.find('(')
			self.Missions.append(Mission(self.Title_Text[:position-1], self.Title_Text[position:]))
		elif self.Rotation:
			self.Rotation = False
			self.Rotation_Number = data
		else:
			if self.Loot == "":
				self.Loot = data
			else:
				self.Loot_Rarity = self.parse_luck(data)
				if self.Rotation_Number is not None:
					self.Missions[-1].add_loot(self.Loot, self.Loot_Rarity, self.Rotation_Number)
				else:
					self.Missions[-1].add_loot(self.Loot, self.Loot_Rarity)
				self.Loot = ""
				self.Loot_Rarity = ""

	def handle_relic(self, data):
		if self.Title:
			self.Title_Text = data
			if self.Title_Text[-8:] != "(Intact)":
				self.Ignore = True
			else:
				self.Ignore = False
				self.Relics.append(Relic(self.Title_Text[:-9]))
		else:
			#  print("{} {}".format(self.Loot, data))
			if self.Ignore:
				return
			if self.Loot == "":
				self.Loot = data
			else:
				self.Loot_Rarity = data
				self.Relics[-1].add_level(Relic.RARITY_NAME[self.Loot_Rarity], self.Loot)
				self.Loot = ""
				self.Loot_Rarity = ""

	def handle_data(self, data):
		if self.Table_number == 1:
			self.handle_mission(data)
		elif self.Table_number == 2:
			self.handle_relic(data)


def extract():
	try:
		response = requests.get("https://n8k6e2y6.ssl.hwcdn.net/repos/hnfvc0o3jnfvc873njb03enrf56.html")
	except requests.ConnectionError:
		return "ConnectionError"
	except requests.HTTPError:
		return "HTTPError"
	except requests.TooManyRedirects:
		return "TooManyRedirects"
	except requests.URLRequired:
		return "URLRequired"
	except requests.RequestException:
		return "RequestException"
	if response.status_code == 200:
		parser = MyHTMLParser()
		parser.feed(response.text)
		parser.mark_vaulted()
		return {'Relics': parser.Relics, 'Missions': parser.Missions}
	else:
		return "error"
