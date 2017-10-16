import datetime
from app.models import db
from app.models.ticket import Ticket

'''
Seeder class for TicketTweak
'''




class TicketTweakSeeder():
    @staticmethod
    def run():
        for i in range (0,5):
            ticket = db.session.query(Ticket).filter_by(id=i)
            ticket.update({
                'updated_at': datetime.datetime.now(),
                'type': 'user'
            })
            db.session.commit()
