import datetime

from app.models import db
from app.models.base_model import BaseModel


class Payment(db.Model, BaseModel):

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
        order_id = db.Column(
                db.Integer,
                db.ForeignKey('orders.id'),
                nullable=False
        )
        order = db.relationship('Order')
        created_at = db.Column(db.DateTime)
        updated_at = db.Column(db.DateTime)

        def __init__(self):
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()

