import datetime
from app.models import db
from app.configs.constants import ROLE
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.booth_checkins import BoothCheckin
from app.models.user import User
from app.models.user_booth import UserBooth
from app.models.partner_pj import PartnerPj
from app.models.questioner_answer import QuestionerAnswer
from app.builders.response_builder import ResponseBuilder


class BoothCheckinService():

	def get_booth_id(self, user):
		role = ''
		if user.role_id == ROLE['booth']:
			# grab booth guests
			role = 'booth'
			booth = db.session.query(UserBooth).filter(UserBooth.user_id == user.id).first()
			if booth is None:
				return response.set_error(True).set_message('Booth not found').build()
			booth_id = booth.booth_id
		elif user.role_id == ROLE['partner']:
			role = 'partner'
			booth = db.session.query(PartnerPj).filter(PartnerPj.user_id == user.id).first()
			if booth is None:
				return response.set_error(True).set_message('Booth not found').build()
			booth_id = booth.partner_id
		return role, booth_id

	def get_guests(self, user):
		response = ResponseBuilder()
		role, booth_id = self.get_booth_id(user)
		guests = db.session.query(BoothCheckin).filter(BoothCheckin.booth_type == role, BoothCheckin.booth_id == booth_id).all()
		_results = []
		for guest in guests:
			data = guest.user.include_photos().as_dict()
			data['checkin_details'] = guest.as_dict()
			answer = self.get_questioner_answer(guest.user.id)
			data['speed_dating'] = answer.as_dict() if answer else None
			_results.append(data)
		return response.set_data(_results).set_message('guests retrieved successfully').build()

	def get_questioner_answer(self, user_id):
		return db.session.query(QuestionerAnswer).filter(QuestionerAnswer.user_id == user_id).first()

	def filter_guests(self, user, filter):
		response = ResponseBuilder()
		role, booth_id = self.get_booth_id(user)
		guests = db.session.query(BoothCheckin).filter(BoothCheckin.booth_type == role, BoothCheckin.booth_id == booth_id, BoothCheckin.speed_dating == filter).all()
		_results = []
		for guest in guests:
			data = guest.user.include_photos().as_dict()
			data['checkin_details'] = guest.as_dict()
			_results.append(data)
		return response.set_data(_results).set_message('guests retrieved successfully').build()


	def checkin(self, payloads):
		response = ResponseBuilder()
		# check if checkedin
		checkedin = db.session.query(BoothCheckin).filter(BoothCheckin.user_id == payloads['user_id'], BoothCheckin.booth_type == payloads['booth_type'], BoothCheckin.booth_id == payloads['booth_id'])
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
