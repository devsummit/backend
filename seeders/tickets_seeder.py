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
        daily_ticket_a = Ticket()
        daily_ticket_b = Ticket()
        daily_ticket_c = Ticket()
        community_ticket = Ticket()

        full_ticket.ticket_type = 'full'
        daily_ticket_a.ticket_type = 'daily-13'
        daily_ticket_b.ticket_type = 'daily-14'
        daily_ticket_c.ticket_type = 'daily-15'
        community_ticket.ticket_type = 'community'

        full_ticket.price = 400000
        daily_ticket_a.price = 200000
        daily_ticket_b.price = 300000
        daily_ticket_c.price = 350000
        community_ticket.price = 0

        full_ticket.information = 'Ticket for full 3 days devsummit event.'
        daily_ticket_a.information = 'Ticket for 13th November at devsummit event.'
        daily_ticket_b.information = 'Ticket for 14th November at devsummit event.'
        daily_ticket_c.information = 'Ticket for 15th November at devsummit event.'
        community_ticket.information = 'Ticket for community, only given by admin.'
        db.session.add(full_ticket)
        db.session.add(daily_ticket_a)
        db.session.add(daily_ticket_b)
        db.session.add(daily_ticket_c)
        db.session.add(community_ticket)

        db.session.commit()
