import datetime

from app.models import db
from app.models.base_model import BaseModel


class UserFeedback(db.Model, BaseModel):

    # table name
    __tablename__ = 'user_feedbacks'
    # displayed fields
    visible = ['id', 'user_id', 'content', 'created_at', 'updated_at']

    # columns definitions
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
