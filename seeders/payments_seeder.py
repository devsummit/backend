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
        transaction_statuses = ['capture', 'authorize', 'deny']
        statuses = ['accept', 'challenge', 'deny']
        payment_types = ['bank_transfer', 'credit_card']
        banks = ['bri', 'bni', 'permata', 'maybank', 'mandiri', 'bca', 'cimb']
        range_start = 10 ** (7 - 1)
        range_end = (10 ** 7) - 1

        for i in range(0, 10):
            order_id = random.choice(orders)['id']
            saved_token_id = randint(range_start, range_end)
            transaction_id = randint(range_start, range_end)
            gross_amount = randint(range_start, range_end)
            transaction_time = fake.sentence(  
                nb_words=6, variable_nb_words=True, ext_word_list=None
            )
            transaction_status = transaction_statuses[randint(0, 2)]
            masked_card = randint(range_start, range_end)
            payment_type = payment_types[randint(0, 1)]
            bank = banks[randint(0, 6)]
            fraud_status = statuses[randint(0, 2)] 

            new_payment = Payment()
            new_payment.order_id = order_id
            new_payment.saved_token_id = saved_token_id
            new_payment.transaction_id = transaction_id
            new_payment.gross_amount = gross_amount
            new_payment.transaction_time = transaction_time
            new_payment.transaction_status = transaction_status
            new_payment.masked_card = masked_card
            new_payment.payment_type = payment_type
            new_payment.bank = bank
            new_payment.fraud_status = fraud_status
            db.session.add(new_payment)
            db.session.commit()
