import datetime
from sqlalchemy import text
from app.models import db
# import model class
from app.services.base_service import BaseService

class OverviewService(BaseService):

    def getAttendees(self):
        t = db.engine.execute("select max(created_at) from attendees").first()
        if t and len(t)>0:
            last_date = t[0].isoformat()
        else:
            last_date = now.isoformat()
        new = db.engine.execute('select coalesce(count(*),0) from attendees where created_at >= "' + last_date + '"').first()
        total = db.engine.execute("select coalesce(count(*),0) from attendees").first()
        return {
            'new': int(new[0].__str__()),
            'total': int(total[0].__str__())
        }
    
    def getBooths(self):
        t = db.engine.execute("select max(created_at) from booths").first()
        if t and len(t)>0:
            last_date = t[0].isoformat()
        else:
            last_date = now.isoformat()
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
        if t and len(t)>0:
            last_date = t[0].isoformat()
        else:
            last_date = now.isoformat()
        new = db.engine.execute('select coalesce(count(*),0) from sponsors where created_at >= "' + last_date + '"').first()
        total = db.engine.execute("select coalesce(count(*),0) from sponsors").first()
        return {
            'new': int(new[0].__str__()),
            'total': int(total[0].__str__())
        }