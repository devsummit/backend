import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.booth_checkins import BoothCheckin
from app.builders.response_builder import ResponseBuilder


class BoothCheckinService():

	def get_guests(self, payloads):
		pass

	def checkin(self, payloads):
		response = ResponseBuilder()
		# check if checkedin
		checkedin = db.session.query(BoothCheckin).filter(BoothCheckin.user_id == payloads['user_id'])
		if checkedin.first():
			return response.set_data(None).set_message('User already checked in').build()
		checkin = BoothCheckin()
		checkin.user_id = payloads['user_id']
		checkin.booth_type = payloads['booth_type']
		checkin.booth_id = payloads['booth_id']
		checkin.speed_dating = payloads['speed_dating']
		db.session.add(checkin)
		try:
			db.session.commit()
			return response.set_data(checkin.as_dict()).set_message('user successfully checked in').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).set_message('sql error').build()
