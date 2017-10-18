import datetime

from app.models import db
from app.models.base_model import BaseModel


class BoothGallery(db.Model, BaseModel):

    #table name
    __tablename__ = 'booth_gallery'
    # displayed fields
    visible = ['id', 'booth_id', 'url', 'updated_at', 'created_at']

    #columns definitions
    id = db.Column(db.Integer,primary_key=True)
    booth_id = db.Column(
        db.String(40),
        db.ForeignKey('booths.id'),
        nullable=False
    )
    url = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
    