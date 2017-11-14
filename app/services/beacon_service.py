import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder
# import model class
from app.models.beacon import Beacon
from app.models.sponsor import Sponsor
from app.models.speaker import Speaker
from app.models.booth import Booth
from app.models.booth_gallery import BoothGallery
from app.models.beacon_map_version import BeaconMapVersion


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

	def is_beacon_exist(self, major, minor):
		beacon = db.session.query(Beacon).filter(Beacon.major == major, Beacon.minor == minor).first()
		if beacon:
			return True
		return False

	def update_map_version(self):
		version = db.session.query(BeaconMapVersion)
		if version.first():
			version.update({
				'version': version.first().version + 1
			})
		else:
			version = BeaconMapVersion()
			version.version = 1
			db.session.add(version)
		db.session.commit()

	def create(self, payloads):
		response = ResponseBuilder()
		if self.is_beacon_exist(payloads['major'], payloads['minor']):
			return response.set_data(None).set_message('duplicate beacon found').set_error(True).build()
		self.model_beacon = Beacon()
		self.model_beacon.major = payloads['major']
		self.model_beacon.minor = payloads['minor']
		self.model_beacon.type = payloads['type']
		self.model_beacon.type_id = payloads['type_id']
		self.model_beacon.description = payloads['description']
		db.session.add(self.model_beacon)
		try:
			db.session.commit()
			self.update_map_version()			
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
				'major': payloads['major'],
				'minor': payloads['minor'],
				'type': payloads['type'],
				'type_id': payloads['type_id'],
				'description': payloads['description'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			self.update_map_version()			
			data = self.model_beacon.first().as_dict()
			return response.set_data(data).set_message('region updated succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).set_message('sql error').build()

	def get_current_version(self):
		return db.session.query(BeaconMapVersion).first().version

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

	def fetch_mapping(self, version):
		response = ResponseBuilder()
		result = []
		current_version = self.get_current_version()
		if version == current_version:
			return response.set_data({'newest': True}).set_message('your beacon map version is already the newest').build()
		# fetch all row from beacon map
		beacons = db.session.query(Beacon).all()
		# for each beacon map include all data neccessary according to their type and type id
		for beacon in beacons:
			data = beacon.as_dict()
			data['details'] = self.include_data(beacon)
			result.append(data)
		result.append({'version': self.get_current_version()})
		# return response
		return response.set_data(result).set_message('You have updated your beacon map to version: %s' %current_version).build()


	def include_data(self, beacon):
		result = {}
		if beacon.type == 'exhibitor':
			exhibitor = db.session.query(Booth).filter(Booth.id == beacon.type_id).first()
			gallery = self.fetch_booth_gallery(exhibitor.id)
			result['exhibitor'] = exhibitor.as_dict()
			result['exhibitor']['gallery'] =[]
			for image in gallery:
				result['exhibitor']['gallery'].append(image.as_dict())
		elif beacon.type == 'sponsor':
			result['sponsor'] = db.session.query(Sponsor).filter(Sponsor.id == beacon.type_id).first().as_dict()
		elif beacon.type == 'speaker':
			speaker = db.session.query(Speaker).filter(Speaker.id == beacon.type_id).first()
			result['speaker'] = speaker.as_dict()
			result['speaker']['user'] = speaker.user.include_photos().as_dict()
		elif beacon.type == 'other':
			pass
		elif beacon.type == 'entrance':
			pass
		return result

	def fetch_booth_gallery(self, booth_id):
		return db.session.query(BoothGallery).filter(BoothGallery.booth_id == booth_id).all()
