from app.models import db
from app.models.user_ticket import UserTicket
from app.models.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
import datetime


class UserTicketService:

    def show(self, user_id):
        user_tickets = BaseModel.as_list(db.session.query(UserTicket).filter_by(user_id=user_id).all())
        if user_tickets is not None:
            return user_tickets
        else:
            data = 'data not found'
            return {
                'error': True,
                'data': data
            }   

    def update(self, user_id, payloads):
        ticket_id = payloads['ticket_id']
        user_ticket = db.session.query(UserTicket).filter_by(id=ticket_id).first().as_dict()
        if user_ticket is not None:
            if user_ticket['user_id'] == user_id:
                self.model_user_ticket = db.session.query(UserTicket).filter_by(id=ticket_id)
                try:
                    self.model_user_ticket.update({
                        'user_id': payloads['receiver_id'],
                        'updated_at': datetime.datetime.now()
                    })
                    db.session.commit()
                    data = self.model_user_ticket.first().as_dict()
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
            else:
                data = 'unauthorized'
                return {
                    'error': True,
                    'data': data
                }  
        else:
            data = 'data not found'
            return {
                'error': True,
                'data': data
            }   
