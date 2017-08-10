from faker import Faker
from app.models.ticket_transfer import TicketTransfer
from app.models import db
from random import randint

'''
Seeder class for
'''


class TicketTransfersSeeder():

    @staticmethod
    def run():
        """
        Create 10 Ticket Transfer seeds
        """
        fake = Faker()
        for i in range(0, 10):
            new_transfer = Ticket()
            new_transfer.sender_user_id = randint(1,10)
            new_transfer.receiver_user_id = randint(10,20)
            db.session.add(new_transfer)
            db.session.commit()
