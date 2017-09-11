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
        Create 6 orders seeds
        """
        orders = BaseModel.as_list(db.session.query(Order).all())
        
        tickets = BaseModel.as_list(db.session.query(Ticket).all())

        orderidarr =  [1,1,2,2,3,4]

        ticketid = [2,3,3,4,1,5]
        
        ticketprice = [200000, 300000, 300000, 350000, 400000, 0]

                
        for i in range(0, 6):
            order_id = orderidarr[i]
            ticket_id = ticketid[i]
            ticket_price = ticketprice[i]
            new_orderdetails = OrderDetails()
            new_orderdetails.ticket_id = ticket_id
            new_orderdetails.order_id = order_id
            # Order one or two tickets per order per ticket_id
            new_orderdetails.count = random.randint(1, 2)
            new_orderdetails.price = ticket_price
            db.session.add(new_orderdetails)
            db.session.commit()
