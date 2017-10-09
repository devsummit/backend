import datetime

from app.models.base_model import BaseModel
from app.models import db


class Invoice(db.Model, BaseModel):
    # table name
    __tablename__ = 'invoices'
    # displayed fields
    visible = ['id', 'invoiceable_type', 'invoiceable_id', 'address', 'description', 'total', 'created_at', 'updated_at']

    # columns definitions
    id = db.Column(
        db.String, 
        primary_key=True
    )
    invoiceable_id = db.Column(
        db.Integer,
        nullable=False
    )

    invoiceable_type = db.Column(
        db.String(120),
        nullable=False
    )
    address = db.Column(db.String(255))
    description = db.Column(db.String(255))
    total = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.id = 'dsp-' + datetime.datetime.now().strftime("%Y%m%d.%H%M%S%f")
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
