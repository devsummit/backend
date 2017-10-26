import datetime
import time
from sqlalchemy import text
from app.models import db
# import model class
from app.services.base_service import BaseService
from app.configs.constants import ROLE

class OverviewService(BaseService):

    def getUsers(self):
        total = db.engine.execute('select coalesce(count(*),0) from users where role_id = ' + str(ROLE['user'])).first()
        return {
            'total': int(total[0].__str__())
        }

    def getAttendees(self):
        count = db.engine.execute('select coalesce(count(*),0) from user_tickets where ticket_id < 4').first()
        return {
            'count': int(count[0].__str__()),
        }
    
    def getBooths(self):
        t = db.engine.execute("select max(created_at) from booths").first()
        if t[0]:
            last_date = t[0].isoformat()
        else:
            last_date = time.strftime("%Y/%m/%d")
        new = db.engine.execute('select coalesce(count(*),0) from booths where created_at >= "' + last_date + '"').first()
        total = db.engine.execute("select coalesce(count(*),0) from booths").first()
        return {
            'new': int(new[0].__str__()),
            'total': int(total[0].__str__())
        }

    def getFinances(self):
        income = db.engine.execute("select coalesce(sum(debit),0) from entry_cash_log").first()
        expense = db.engine.execute("select coalesce(sum(credit),0) from entry_cash_log").first()
        return {
            'income': "{0:,.2f}".format(income[0]),
            'expense': "{0:,.2f}".format(expense[0]),
            'balance': "{0:,.2f}".format(income[0]-expense[0])
        }
    
    def getSponsors(self):
        t = db.engine.execute("select max(created_at) from sponsors").first()
        if t[0] and len(t)>0 and isinstance(t[0], datetime.date):
            last_date = t[0].isoformat()
        else:
            last_date = time.strftime("%Y/%m/%d")
        new = db.engine.execute('select coalesce(count(*),0) from sponsors where created_at >= "' + last_date + '"').first()
        total = db.engine.execute("select coalesce(count(*),0) from sponsors").first()
        return {
            'new': int(new[0].__str__()),
            'total': int(total[0].__str__())
        }