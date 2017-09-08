from app.models.base_model import BaseModel
from app.models.user_ticket import UserTicket
from app.models.payment import Payment
from app.models import db


'''
Seeder class for
'''


class UserTicketsSeeder():

    @staticmethod
    def run():
        
        """
        Create UserTicket seeds
        """

        userid = [2, 1, 2, 3]
       
        for i in range(0,4):
            new_user_ticket = UserTicket()
            new_user_ticket.user_id = userid[i]
            
            db.session.add(new_user_ticket)
            db.session.commit()
