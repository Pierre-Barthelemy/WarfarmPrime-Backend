import threading


class Data:

	def __init__(self):
		self.Mutex = threading.Lock()
		self.Data = {}

	def process_data(self, data):
		self.Data = data

	def get_data(self):
		return self.Data
