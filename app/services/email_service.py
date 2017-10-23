from flask_mail import Message


class EmailService():

	def __init__(self):
		self.message = Message()

	def set_subject(self, subject):
		self.message.subject = subject
		return self

	def set_body(self, body):
		self.message.body = body
		return self

	def set_html(self, body):
		self.message.html = body
		return self

	def set_sender(self, sender):
		self.message.sender = sender
		return self

	def set_recipient(self, recipient):
		self.message.add_recipient(recipient)
		return self

	def set_recipients(self, recipients):
		self.message = recipients
		return self

	def build(self):
		return self.message
