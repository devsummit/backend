from faker import Faker
from app.models.base_model import BaseModel
from app.models import db
from app.models.order import Order
from app.models.user import User
import random

'''
Seeder class for
'''


class OrdersSeeder():

    @staticmethod
    def run():
        """
        Create 10 orders seeds
        """
        fake = Faker()
        users = BaseModel.as_list(db.session.query(User).all())
        for i in range(0, 10):
            user_id = random.choice(users)['id']
            status = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None
            )
            new_order = Order()
            new_order.user_id = user_id
            new_order.status = status
            db.session.add(new_order)
            db.session.commit()
