from faker import Faker
from random import randint
import random
from app.models.base_model import BaseModel
from app.models.payment import Payment
from app.models import db
from app.models.order import Order

'''
Seeder class for
'''


class PaymentsSeeder():

    @staticmethod
    def run():
        """
        Create 10 Payments seeds
        """
        fake = Faker()
        orders = BaseModel.as_list(db.session.query(Order).all())
        range_start = 10 ** ( 7 - 1 )
        range_end = ( 10 ** 7 ) - 1

        for i in range(0, 10):
            card_id = randint(range_start, range_end)
            total = randint(range_start, range_end)
            additional_information = fake.sentence(
                    nb_words=10, variable_nb_words=True, ext_word_list=None
            )
            sender = fake.sentence(
                    nb_words=6, variable_nb_words=True, ext_word_list=None
            )
            order_id = random.choice(orders)['id']
            new_payment = Payment()
            new_payment.card_id = card_id
            new_payment.total = total
            new_payment.additional_information = additional_information
            new_payment.sender = sender
            db.session.add(new_payment)
            db.session.commit()


