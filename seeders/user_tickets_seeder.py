from app.models.user_ticket import UserTicket
from app.models import db
from random import randint

'''
Seeder class for
'''


class UserTicketsSeeder():

    @staticmethod
    def run():
        """
        Create 10 UserTicket seeds
        """

        for i in range(0, 10):
            new_user_ticket = UserTicket()
            new_user_ticket.user_id = i + 1
            new_user_ticket.ticket_id = randint(1, 3)
            db.session.add(new_user_ticket)
            db.session.commit()
