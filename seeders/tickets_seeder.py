from app.models.ticket import Ticket
from app.models import db

'''
Seeder class for
'''


class TicketsSeeder():

    @staticmethod
    def run():
        """
        Create 4 Ticket seeds
        """

        full_ticket = Ticket()
        daily_ticket = Ticket()
        community_ticket = Ticket()

        full_ticket.ticket_type = 'full'
        daily_ticket.ticket_type = 'daily'
        community_ticket.ticket_type = 'community'

        full_ticket.price = 400000
        daily_ticket.price = 200000
        community_ticket.price = 0

        full_ticket.information = 'Ticket for full 3 days devsummit event.'
        daily_ticket.information = 'Ticket for 1 day at devsummit event.'
        community_ticket.information = 'Ticket for community, only given by admin.'
        db.session.add(full_ticket)
        db.session.add(daily_ticket)
        db.session.add(community_ticket)

        db.session.commit()
