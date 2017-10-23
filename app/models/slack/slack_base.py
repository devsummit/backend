class SlackBase():

	def __init__(self):
		self.message = '@channel\n' + self.headers + '\n'

	def build(self):
		return self.message;

