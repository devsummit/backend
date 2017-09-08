from app.models.ticket_transfer_log import TicketTransferLog
from app.models import db

'''
Seeder class for
'''


class TicketTransferLogsSeeder():

    # @staticmethod
    # def run():
    #     """
    #     Create 5 Ticket Transfer seeds
    #     """
    #     for i in range(0, 5):
    #         new_transfer = TicketTransferLog()
    #         new_transfer.user_ticket_id = i + 1
    #         new_transfer.sender_user_id = i + 1
    #         new_transfer.receiver_user_id = i + 11
    #         db.session.add(new_transfer)
    #         db.session.commit()
