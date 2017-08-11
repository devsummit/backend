import datetime

from app.models import db
from app.models.base_model import BaseModel


class UserPhoto(db.Model, BaseModel):
    __tablename__ = 'user_photo'

    visible = ['id', 'user_id', 'url', 'created_at', 'updated_at']
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    url = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()