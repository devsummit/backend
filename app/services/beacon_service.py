import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder
# import model class
from app.models.beacon import Beacon


class BeaconService():

	def get(self):
		response = ResponseBuilder()
		beacons = db.session.query(Beacon).all()
		_results = []
		for beacon in beacons:
			_results.append(beacon.as_dict())
		return response.set_data(_results).set_message('region retrieved succesfully').build()

	def show(self, id):
		response = ResponseBuilder()
		beacon = db.session.query(Beacon).filter(Beacon.id == id).first()
		if beacon:
			return response.set_data(beacon.as_dict()).set_message('beacon retrieved succesfully').build()
		return response.set_data(None).set_error(True).set_message('beacon not found').build()

	def is_uuid_exist(self, uuid):
		beacon = db.session.query(Beacon).filter(Beacon.uuid == uuid).first()
		if beacon:
			return True
		return False

	def create(self, payloads):
		response = ResponseBuilder()
		if self.is_uuid_exist(payloads['uuid']):
			return response.set_data(None).set_message('duplicate uuid found').set_error(True).build()
		self.model_beacon = Beacon()
		self.model_beacon.uuid = payloads['uuid']
		self.model_beacon.type = payloads['type']
		self.model_beacon.type_id = payloads['type_id']
		self.model_beacon.description = payloads['description']
		db.session.add(self.model_beacon)
		try:
			db.session.commit()
			data = self.model_beacon.as_dict()
			return response.set_data(data).set_message('region created succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).set_message('sql error').build()

	def update(self, payloads, id):
		response = ResponseBuilder()
		try:
			self.model_beacon = db.session.query(Beacon).filter(Beacon.id == id)
			self.model_beacon.update({
				'uuid': payloads['uuid'],
				'type': payloads['type'],
				'type_id': payloads['type_id'],
				'description': payloads['description'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_beacon.first().as_dict()
			return response.set_data(data).set_message('region updated succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).set_message('sql error').build()

	def delete(self, id):
		response = ResponseBuilder()
		self.model_beacon = db.session.query(Beacon).filter(Beacon.id == id)
		if self.model_beacon.first() is not None:
			# delete row
			self.model_beacon.delete()
			db.session.commit()
			return response.set_data(None).set_message('region row deleted succesfully').build()
		else:
			data = 'data not found'
			return response.set_data(data).set_error(True).set_message('sql error').build()
