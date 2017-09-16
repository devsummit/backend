from app.models.ticket import Ticket
from app.models import db

'''
Seeder class for
'''

class HackatonTicketsSeeder():
    
    @staticmethod
    def run():
        """
        Create 2 Ticket Hackaton seeds
        """

        hackaton_ticket_a = Ticket()
        hackaton_ticket_b = Ticket()

        hackaton_ticket_a.ticket_type = 'hackaton-a'
        hackaton_ticket_b.ticket_type = 'hackaton-b'

        hackaton_ticket_a.price = 5000000
        hackaton_ticket_b.price = 5000000

        hackaton_ticket_a.information = 'Ticket for hackaton day one.'
        hackaton_ticket_b.information = 'Ticket for hackaton day two.'

        db.session.add(hackaton_ticket_a)
        db.session.add(hackaton_ticket_b)

        db.session.commit()
