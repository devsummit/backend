import datetime

from app.models import db
from app.models.base_model import BaseModel

class UserBooth(db.Model, BaseModel):
    __tablename__ = 'user_booth'

    visible = ['id', 'user_id', 'booth_id', 'created_at', 'updated_at']

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    user = db.relationship('User')

    booth_id = db.Column(
        db.Integer,
        db.ForeignKey('booths.id'),
        nullable=False
    )
    booth = db.relationship('Booth')

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
