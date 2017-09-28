from app.models import db
from app.models.booth import Booth
from app.models.user import User
from app.builders.response_builder import ResponseBuilder
from app.models.point_transaction_log import PointTransactionLog
from sqlalchemy.exc import SQLAlchemyError


class PointsTransactionService():

	def transfer_points(self, receiver_id, sender_id, points):
		response = ResponseBuilder()
		# query users
		booth = db.session.query(Booth).filter_by(user_id=sender_id).first()
		user = db.session.query(User).filter_by(id=receiver_id).first()
		# check booth points first
		if booth.points < points:
			return response.set_error(True).set_data('You don\'t have enough point to grant').build()
		# transfer point
		booth.points = booth.points - points
		if user.points:
			user.points = user.points + points
		else:
			user.points = points
		try:
			db.session.commit()
			# log transfer
			transaction_log = PointTransactionLog()
			transaction_log.booth_id = booth.id
			transaction_log.user_id = user.id
			transaction_log.amount = points

			db.session.add(transaction_log)
			db.session.commit()
			# return value
			return response.set_data('Point transfered succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def get_booth_log(self, user_id):
		# get booth id
		booth = db.session.query(Booth).filter_by(user_id=user_id).first()
		# query
		logs = db.session.query(PointTransactionLog).filter_by(booth_id=booth.id).all()
		# return 
		return logs

	def get_user_log(self, user_id):
		# query
		logs = db.session.query(PointTransactionLog).filter_by(user_id=user_id).all()
		return logs

	def get_admin_log(self):
		logs = db.session.query(PointTransactionLog).all()
		return logs
