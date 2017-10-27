from app.models import db
from app.models.user import User
from app.models.payment import Payment
from app.models.slack.slack_base import SlackBase


class SlackVerify(SlackBase):

	def __init__(self, payload):
		self.headers = 'Payment Verification notifications'
		SlackBase.__init__(self)
		self.message = self.message + self.generate_message(payload)

	def generate_message(self, payload):
		user = db.session.query(User).filter_by(id=payload['data']['user_id']).first()
		payment = db.session.query(Payment).filter_by(order_id=payload['data']['order_id']).first()
		currency = 'USD ' if payment.payment_type == 'paypal' else 'IDR '
		message = "username: " + user.username + '\n'
		message += "name: " + (user.first_name + ' ' + user.last_name) + '\n'
		message += "order-id: " + str(payload['data']['id']) + '\n'
		message += "Required payment amount: IDR " + '{:2,.2f}'.format(payment.gross_amount) + '\n'
		message += "proof: " + payload['data']['payment_proof'] + '\n'

		message += "\npayment-type: " + payment.payment_type + '\n'
		return message
