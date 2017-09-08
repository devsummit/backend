from faker import Faker
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

        