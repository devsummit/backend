import datetime

from app.models.base_model import BaseModel
from app.models import db


class RedeemCode(db.Model, BaseModel):
    # table name
    __tablename__ = 'redeem_codes'
    # displayed fields
    visible = ['id', 'codeable_type', 'codeable_id', 'code', 'count']

    # columns definitions
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    codeable_type = db.Column(
        db.String(40),
        nullable=False
    )
    code = db.Column(
        db.String(6),
        nullable=False
    )
    codeable_id = db.Column(
        db.String(40),
        nullable=False
    )
    count = db.Column(db.Integer)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
