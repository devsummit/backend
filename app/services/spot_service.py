import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.spot import Spot


class SpotService():

	def __init__(self, model_spot):
		self.model_spot = model_spot

	def get(self):
		spots = db.session.query(Spot).all()
		return spots

	def update(self, payloads, id):
		try:
			self.model_spot = db.session.query(Spot).filter_by(id=id)
			self.model_spot.update({
				'beacon_id': payloads['beacon_id'],
				'stage_id': payloads['stage_id'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_spot.first().as_dict()
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
