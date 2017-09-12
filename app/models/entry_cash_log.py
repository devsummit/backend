import datetime

from app.models import db
from app.models.base_model import BaseModel


class EntryCashLog(db.Model, BaseModel):

    # table name
    __tablename__ = 'entry_cash_log'
    # display visible field
    visible = [
        'id',
        'expense',
        'income',
        'details',
        'created_at',
        'updated_at'
    ]

    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.Integer)
    income = db.Column(db.Integer)
    details = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
