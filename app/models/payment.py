import datetime

from app.models import db
from app.models.base_model import BaseModel


class Payment(db.Model, BaseModel):

        # table name
        __tablename__ = 'payments'
        # displayed fields
        visible = [
                'id', 
                'order_id',
                'saved_token_id', 
                'transaction_id', 
                'payment_type',
                'gross_amount',
                'transaction_time',
                'transaction_status',
                'masked_card',
                'bank', 
                'fraud_status',
                'created_at', 
                'updated_at'
        ]

        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(
                db.Integer,
                db.ForeignKey('orders.id'),
                nullable=False
        )
        order = db.relationship('Order')
        user_id = db.Column(
            db.String(40),
            db.ForeignKey('users.id'),
            nullable=False
        )
        user = db.relationship('User')
        
        saved_token_id = db.Column(db.Integer)
        transaction_id = db.Column(db.Integer)
        payment_type = db.Column(db.String)
        gross_amount = db.Column(db.Integer)
        transaction_time = db.Column(db.String)
        transaction_status = db.Column(db.String)
        masked_card = db.Column(db.String)
        bank = db.Column(db.String)
        fraud_status = db.Column(db.String)
        created_at = db.Column(db.DateTime)
        updated_at = db.Column(db.DateTime)

        def __init__(self):
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
