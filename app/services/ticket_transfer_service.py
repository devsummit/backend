import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.user_ticket import UserTicket
from app.models.ticket_transfer_log import TicketTransferLog


class TicketTransferService():

    # query = meta.Session.query(User).filter(or_(User.firstname.like(searchVar),User.lastname.like(searchVar)))

    def get_logs(self, user_id=''):
        if user_id == '':
            transferslogs = db.session.query(TicketTransferLog).all()
        else:
            transferslogsends = db.session.query(TicketTransferLog).filter(TicketTransferLog.sender_user_id==user_id)
            transferslogreceives = db.session.query(TicketTransferLog).filter(TicketTransferLog.sender_user_id==user_id)
            transferslogs = transferslogsends.union(transferslogreceives)

        return transferslogs

    def show(self, id):
        pass

    def create(self, payloads):
        pass
