import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.user_ticket import UserTicket
from app.models.ticket_transfer_log import TicketTransferLog


class TicketTransferService():
    
    def get(self):
        transferslogs = db.session.query(TicketTransferLog).all()
        return transferslogs

    def show(self, id):
        pass

    def create(self, payloads):
        pass
    
