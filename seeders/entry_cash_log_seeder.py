from random import randint
from app.models.entry_cash_log import EntryCashLog 
from app.models import db
import datetime
from faker import Faker

'''
Seeder class for
'''


class EntryCashLogSeeder():

    @staticmethod
    def run():
        """
        Create 4 Entry Cash Log seeds
        """
        new_entry_cash_log_1 = EntryCashLog()
        new_entry_cash_log_1.expense = 0
        new_entry_cash_log_1.income = 1500000
        new_entry_cash_log_1.details = 'Buy event organizer goods'
        db.session.add(new_entry_cash_log_1)
        
        new_entry_cash_log_2 = EntryCashLog()
        new_entry_cash_log_2.expense = 30000000
        new_entry_cash_log_2.income = 0
        new_entry_cash_log_2.details = 'Buy 3 drone for day 3 party'
        db.session.add(new_entry_cash_log_2)

        new_entry_cash_log_3 = EntryCashLog()
        new_entry_cash_log_3.expense = 0
        new_entry_cash_log_3.income = 90000000
        new_entry_cash_log_3.details = 'Sponsorship from google'
        db.session.add(new_entry_cash_log_3)
        
        db.session.commit()