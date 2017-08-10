from faker import Faker
from app.models.ticket import Ticket
from app.models import db
from random import randint

'''
Seeder class for
'''


class UsersSeeder():

    @staticmethod
    def run():
        """
        Create 20 Users seeds
        """
        fake = Faker()
        for i in range(0, 20):
            new_ticket = Ticket()
            new_ticket.ticket_type = fake.random_element(elements=('gold', 'silver', 'ruby'))
            new_ticket.price = fake.price()
            new_ticket.information = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            db.session.add(new_ticket)
            db.session.commit()
