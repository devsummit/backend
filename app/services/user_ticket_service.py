import datetime
from app.models import db
from app.models.user_ticket import UserTicket
from app.models.check_in import CheckIn
from app.models.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError


class UserTicketService:

    def check_in(self, user_ticket_id):
        exist = db.session.query(UserTicket).filter_by(id=user_ticket_id).first()
        if exist is None:
            return {
                'data': {'exist': False},
                'message': 'user ticket does not exist'
            }

        ticket = exist.ticket
        if ticket.ticket_type == 'full':
            checked_in = db.session.query(CheckIn).filter_by(user_ticket_id=user_ticket_id)
            if checked_in.first() is not None:
                # update updated at
                checked_in.update({
                    'updated_at': datetime.datetime.now()
                    })
                try:
                    db.session.commit()
                    return {
                        'error': False,
                        'data': {'checked_in': True},
                        'message': 'user checked in successfully'
                    }
                except SQLAlchemyError as e:
                    data = e.orig.args
                    return {
                        'error': True,
                        'data': {'sql_error': True},
                        'message': data
                    }
            # else check in
            return self.create_checkin(user_ticket_id)

        # else if ticket type is daily
        checked_in = db.session.query(CheckIn).filter_by(user_ticket_id=user_ticket_id).first()
        # check if ticket id already in checkin
        if checked_in is None:
            # checkin user
            return self.create_checkin(user_ticket_id)

        # else return user already checked in, ticket is expired
        return {
            'error': True,
            'data': {'expired': True},
            'message': 'Ticket has been checked in, cannot be used anymore'
        }

    def create_checkin(self, user_ticket_id):
        check_in = CheckIn()
        check_in.user_ticket_id = user_ticket_id
        db.session.add(check_in)
        try:
            db.session.commit()
            # return checkin success
            return {
                'error': False,
                'data': {'checked_in': True},
                'message': 'user checked in successfully'
            }
        except SQLAlchemyError as e:
            data = e.orig.args
            return {
                'error': True,
                'data': {'sql_error': True},
                'message': data
            }

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
