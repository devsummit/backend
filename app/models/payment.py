import datetime

from app.models import db
from app.model.base_models import BaseModel


class Payment(db.model, BaseModel):

        # table name
        __tablename__ = 'payments'
        # displayed fields
        visible = [
                'id', 
                'card_id', 
                'total', 
                'additional_information', 
                'sender', 
                'order_id', 
                'created_at', 
                'updated_at'
        ]

        id = db.Column(db.Integer, primary_key=True)
        card_id = db.Column(db.Integer)
        total = db.Column(db.Integer)
        additional_information = db.Column(db.String)
        sender = db.Column(db.String)
        order_id = db.Column(db.Integer)
        created_at = db.Column(db.Datetime)
        updated_at = db.Column(db.Datetime)

        def __init__(self):
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()

