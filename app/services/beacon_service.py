import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.beacon import Beacon


class BeaconService():

	def get(self):
		beacons = db.session.query(Beacon).all()
		return beacons

	def create(self, payloads):
		self.model_beacon = Beacon()
		self.model_beacon.code = payloads['code']
		db.session.add(self.model_beacon)
		try:
			db.session.commit()
			data = self.model_beacon.as_dict()
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
			self.model_beacon = db.session.query(Beacon).filter_by(id=id)
			self.model_beacon.update({
				'code': payloads['code'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_beacon.first().as_dict()
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
		self.model_beacon = db.session.query(Beacon).filter_by(id=id)
		if self.model_beacon.first() is not None:
			# delete row
			self.model_beacon.delete()
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
