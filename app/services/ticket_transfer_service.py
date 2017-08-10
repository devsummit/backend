import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.ticket_transfer import TicketTransfer


class TicketTransferService():