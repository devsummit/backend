from app.models.base_model import BaseModel
from app.models import db
from app.models.order import Order
from app.models.user import User
from app.models.payment import Payment
import random

'''
Seeder class for
'''


class OrdersSeeder():

    @staticmethod
    def run():
        """
        Create 4 orders seeds
        """

        payments = BaseModel.as_list(db.session.query(Payment).all())
        userid = [1, 2, 2, 3]
        status = ['reserved', 'confirmed', 'reserved', 'confirmed']

        for i in range(0, 4):
            orderrow = Order()
            orderrow.user_id = userid[i]
            orderrow.status = status[i]
            db.session.add(orderrow)
            db.session.commit()

        


        

        # fake = Faker()
        # users = BaseModel.as_list(db.session.query(User).all())
        # for i in range(0, 4):
        #     user_id = random.choice(users)['id']
        #     # The status of each order is either Reserved or Confirmed
        #     status = random.choice(['Reserved', 'Confirmed'])
        #     # status = fake.sentence(
        #     #     nb_words=6, variable_nb_words=True, ext_word_list=None
        #     # )
        #     new_order = Order()
        #     new_order.user_id = user_id
        #     new_order.status = status
        #     db.session.add(new_order)
        #     db.session.commit()