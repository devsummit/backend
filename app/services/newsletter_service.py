import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.newsletter import Newsletter


class NewsletterService():

	def get(self):
		subscribers = db.session.query(Newsletter).all()
		return subscribers

	def show(self, id):
		subscriber = db.session.query(Newsletter).filter_by(id=id).first()
		return subscriber

	def create(self, payloads):
		self.model_newsletter = Newsletter()
		self.model_newsletter.email = payloads['email']
		db.session.add(self.model_newsletter)
		try:
			db.session.commit()
			data = self.model_newsletter.as_dict()
			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def update(self, payloads, id):
		try:
			self.model_newsletter = db.session.query(Newsletter).filter_by(id=id)
			self.model_newsletter.update({
				'email': payloads['email'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_newsletter.first().as_dict()
			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def delete(self, id):
		self.model_newsletter = db.session.query(Newsletter).filter_by(id=id)
		if self.model_newsletter.first() is not None:
			# delete row
			self.model_newsletter.delete()
			db.session.commit()
			return {
				'error': False,
				'data': None
			}
		else:
			data = 'data not found'
			return {
				'error': True,
				'data': data
			}
