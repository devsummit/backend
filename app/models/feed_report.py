from datetime import datetime, timedelta
from app.models.base_model import BaseModel
from app.models import db


class FeedReport(db.Model, BaseModel):

    __tablename__ = 'feed_reports'

    visible = ['id', 'user_id', 'type', 'feed_id', 'created_at', 'updated_at']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    type = db.Column(db.String)
    feed_id = db.Column(
        db.Integer,
        db.ForeignKey('feeds.id'),
        nullable=False
    )
    user = db.relationship('User')
    feed = db.relationship('Feed')
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.now() + timedelta(hours=7) 
        self.updated_at = datetime.now() + timedelta(hours=7)
