import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
# import model class
from app.models.user_ticket import UserTicket
from app.models.user import User
from app.builders.response_builder import ResponseBuilder
from app.models.ticket_transfer_log import TicketTransferLog
from app.models.base_model import BaseModel


class TicketTransferService():

	def get_logs(self, user_id=''):
		response = ResponseBuilder()
		if user_id == '':
			transferslogsraw = db.session.query(TicketTransferLog).all()
			transferslogsraw2 = self.transformTable(transferslogsraw)
			transferslogs = self.transformTimeZone(transferslogsraw2)					
		else:
			transferslogsends = db.session.query(TicketTransferLog).filter(
				TicketTransferLog.sender_user_id == user_id)
			transferslogreceives = db.session.query(TicketTransferLog).filter(
				TicketTransferLog.receiver_user_id == user_id)
			transferslogsraw = transferslogsends.union(transferslogreceives)
			transferslogsraw2 = self.transformTable(transferslogsraw)
			transferslogs = self.transformTimeZone(transferslogsraw2)
		return transferslogs

	def transfer(self, user_id, user_ticket_id, receiver):
		response = ResponseBuilder()
		userticket = db.session.query(UserTicket).filter_by(id=user_ticket_id)
		if userticket.first() is None:
			return response.set_error(True).set_data(None).set_message('ticket not found').build()

		if userticket.first().as_dict()['user_id'] != user_id:
			return response.set_error(True).set_data(None).set_message('this ticket is not yours').build()

		receiver_raw = db.session.query(User).filter(or_(User.username.like(receiver), User.email.like(receiver))).first()

		if receiver_raw is None:
			return response.set_error(True).set_data(None).set_message('receiver could not be found').build()
		receiver_id = receiver_raw.as_dict()['id']
		try:
			# update user ticket
			userticket.update({
				'user_id': receiver_id,
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()

			# add transfer log
			transferlog = TicketTransferLog()
			transferlog.sender_user_id = user_id
			transferlog.receiver_user_id = receiver_id
			# transferlog.user_ticket_id = 1
			transferlog.user_ticket_id = user_ticket_id
			db.session.add(transferlog)

			db.session.commit()
			data = transferlog.as_dict()
			for key in data.keys():
				if key in ['receiver', 'sender']:
					temp_dict = data[key].as_dict()
					data[key] = temp_dict 
			return response.set_data(data).set_message('ticket transfered successfully').build()

		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(None).set_message(data).set_error(True).build()

	def transformTable(self, obj):
		transferslogs = BaseModel.as_list(obj)		
		for entry in transferslogs:
			for key in entry.keys():
				if key in ['receiver', 'sender']:
					temp_dict = entry[key].as_dict()
					entry[key] = temp_dict
					continue
		return transferslogs

	def transformTimeZone(self, obj):
		log_list = obj
		for entry in log_list:
			created_at_timezoned = datetime.datetime.strptime(entry['created_at'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=7)
			entry['created_at'] = str(created_at_timezoned).rsplit('.', maxsplit=1)[0]
			updated_at_timezoned = datetime.datetime.strptime(entry['updated_at'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=7)
			entry['updated_at'] = str(updated_at_timezoned).rsplit('.', maxsplit=1)[0]
		return log_list

