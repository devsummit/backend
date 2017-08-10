import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.user_ticket import UserTicket
from app.models.ticket_transfer_log import TicketTransferLog


class TicketTransferService():

    def get_logs(self, user_id=''):
        if user_id == '':
            transferslogs = db.session.query(TicketTransferLog).all()
        else:
            transferslogsends = db.session.query(TicketTransferLog).filter(TicketTransferLog.sender_user_id==user_id)
            transferslogreceives = db.session.query(TicketTransferLog).filter(TicketTransferLog.sender_user_id==user_id)
            transferslogs = transferslogsends.union(transferslogreceives)

        return transferslogs


    def transfer(self, user_id, user_ticket_id, receiver_id):
        if (user_id == '' or user_ticket_id==''  or receiver_id==''):
            return {
				'error': True,
				'data': 'sender_id, user_ticket_id or receiver_id is not valid'
			}

        userticket = db.session.query(UserTicket).filter_by(id=user_ticket_id)
        if userticket.count()<=0:
            return {
                'error': True,
                'data': 'ticket not found'
            }

        try:            
            # update user ticket
            userticket.update({
                'user_id': receiver_id,
                'updated_at': datetime.datetime.now()
            })
            db.session.commit()

            # add transfer log
            transferlog = TicketTransferLog()
            transferlog.sender_user_id =  user_id
            transferlog.receiver_user_id =  receiver_id
            # transferlog.user_ticket_id = 1
            transferlog.user_ticket_id = user_ticket_id
            db.session.add(transferlog)

            db.session.commit()
            data = transferlog.as_dict()
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
            
