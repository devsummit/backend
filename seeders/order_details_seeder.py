from app.models.base_model import BaseModel
from app.models import db
from app.models.order import Order
from app.models.order_details import OrderDetails
from app.models.ticket import Ticket
import random

'''
Seeder class for
'''


class OrdersDetailsSeeder():

    @staticmethod
    def run():
        """
        Create 10 orders seeds
        """
        orders = BaseModel.as_list(db.session.query(Order).all())
        # print(orders)
        tickets = BaseModel.as_list(db.session.query(Ticket).all())
        for i in range(0, 10):
            order_id = random.choice(orders)['id']
            ticket = random.choice(tickets)
            ticket_id = ticket['id']
            ticket_price = ticket['price']
            new_orderdetails = OrderDetails()
            new_orderdetails.ticket_id = ticket_id
            new_orderdetails.order_id = order_id
            new_orderdetails.count = random.randint(1,6)
            new_orderdetails.price = ticket_price
            db.session.add(new_orderdetails)
            db.session.commit()
