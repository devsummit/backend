from app.models.slack.slack_base import SlackBase

class SlackOrder(SlackBase):

	def __init__(self, user, order, payment_type):
		self.headers = 'Order notifications'
		SlackBase.__init__(self)
		self.message = self.message + self.generate_message(user, order, payment_type)

	def generate_message(self, user, order, payment_type):
		currency = 'USD ' if payment_type == 'paypal' else 'IDR '
		message = "username: " + user['username'] + '\n'
		message += "name: " + (user['first_name'] + ' ' + user['last_name']) + '\n'
		message += "order-id: " + order['data']['id'] + '\n'
		message += 'Details\n\n'
		for item in order['included']:
			message += "ticket-id: " + str(item['ticket_id']) + '\n'
			message += "count: " + str(item['count']) + '\n'
			message += "price: " + currency + '{:2,.2f}'.format((item['count'] * item['price'])) + '\n' 
		message += "\npayment-type: " + payment_type + '\n'
		return message