import datetime

from app.models import db
from app.models.base_model import BaseModel
from app.models.source import Source


class EntryCashLog(db.Model, BaseModel):

    # table name
    __tablename__ = 'entry_cash_log'
    # display visible field
    visible = ['id', 'source_id', 'debit', 'credit', 'description', 'created_at', 'updated_at']

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(
        db.String(40),
        db.ForeignKey('sources.id'),
        nullable=False
    )
    source = db.relationship('Source')
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
