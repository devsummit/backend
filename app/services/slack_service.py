import requests
from app.configs.constants import SLACK

class SlackService():

	def __init__(self):
		self.headers = {
			'Content-type': 'application/json'
		}

	def send_message(self, message):
		result = requests.post(SLACK['hook'], headers=self.headers, json={'text': message})
