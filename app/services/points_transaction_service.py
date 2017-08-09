from app.models import db
from app.models.booth import Booth
from app.models.attendee import Attendee
from app.models.point_transaction_log import PointTransactionLog
from sqlalchemy.exc import SQLAlchemyError


class PointsTransactionService():

	def transfer_points(self, receiver_id, sender_id, points):
		# query users
		booth = db.session.query(Booth).filter_by(user_id=sender_id).first()
		attendee = db.session.query(Attendee).filter_by(user_id=receiver_id).first()
		# check booth points first
		if booth.points < points:
			return {
				'error': True,
				'data': 'You don\'t have enough point to grant'
			}
		# transfer point
		booth.points = booth.points - points
		attendee.points = attendee.points + points
		try:
			db.session.commit()
			# log transfer
			transaction_log = PointTransactionLog()
			transaction_log.booth_id = booth.id
			transaction_log.attendee_id = attendee.id
			transaction_log.amount = points

			db.session.add(transaction_log)
			db.session.commit()
			# return value
			return {
				'error': False,
				'data': 'Point transfered succesfully'
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def get_booth_log(self, user_id):
		# get booth id
		booth = db.session.query(Booth).filter_by(user_id=user_id).first()
		# query
		logs = db.session.query(PointTransactionLog).filter_by(booth_id=booth.id).all()
		# return 
		return logs

	def get_attendee_log(self, user_id):
		# get booth id
		attendee = db.session.query(Attendee).filter_by(user_id=user_id).first()
		# query
		logs = db.session.query(PointTransactionLog).filter_by(attendee_id=attendee.id).all()
		return logs

	def get_admin_log(self):
		logs = db.session.query(PointTransactionLog).all()
		return logs
