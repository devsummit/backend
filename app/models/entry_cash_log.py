import datetime

from app.models import db
from app.models.base_model import BaseModel


class EntryCashLog(db.Model, BaseModel):

    # table name
    __tablename__ = 'entry_cash_log'
    # display visible field
    visible = [
        'id',
        'amount',
        'description',
        'created_at',
        'updated_at'
    ]

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
