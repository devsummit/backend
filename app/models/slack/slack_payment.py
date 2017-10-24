from app.models.slack.slack_base import SlackBase


class SlackPayment(SlackBase):

	def __init__(self, user, payment, paypal):
		self.headers = 'Payment Notification'
		SlackBase.__init__(self)
		self.message = self.message + self.generate_message(user, payment, paypal)


	def generate_message(self, user, payment, paypal):		
		message = ''
		if paypal:
			message += 'Paypal transaction-id: ' + payment['transaction_id'] + '\n'
		message += 'order-id: ' + payment['order_id'] + '\n'
		message += 'username: ' + user.username + '\n'
		message += 'Just completed his / her payment \n'
		return message