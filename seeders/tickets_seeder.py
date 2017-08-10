from faker import Faker
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
        TICKET = dict([('gold', 150000), ('ruby', 100000),
                       ('siver', 50000), ('bacan', 25000)])

        fake = Faker()

        for key, value in TICKET.items():
            new_ticket = Ticket()

            new_ticket.ticket_type = key

            new_ticket.price = value

            new_ticket.information = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None)
            db.session.add(new_ticket)
            db.session.commit()