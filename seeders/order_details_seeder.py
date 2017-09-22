from app.models import db
from app.models.order_details import OrderDetails
import random
from app.models.order import Order
from app.models.base_model import BaseModel

'''
Seeder class for
'''


class OrdersDetailsSeeder():

    @staticmethod
    def run():
        """
        Create 6 orders seeds
        """

        orders = BaseModel.as_list(db.session.query(Order).all())
        ticketid = [2, 3, 3, 4, 1, 5]
        
        ticketprice = [200000, 300000, 300000, 350000, 400000, 0]

        for i in range(0, 6):
            order_id = random.choice(orders)['id']
            ticket_id = ticketid[i]
            ticket_price = ticketprice[i]
            # ticket = random.choice(tickets)
            # tickets['id']
            # ticket_id = ticket['id']
            # ticket_price = ticket['price']
            new_orderdetails = OrderDetails()
            new_orderdetails.ticket_id = ticket_id
            new_orderdetails.order_id = order_id
            # Order one or two tickets per order per ticket_id
            new_orderdetails.count = random.randint(1, 2)
            new_orderdetails.price = ticket_price
            db.session.add(new_orderdetails)
            db.session.commit()
