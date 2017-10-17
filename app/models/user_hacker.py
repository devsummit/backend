import datetime

from app.models.base_model import BaseModel
from app.models import db


class HackerTeam(db.Model, BaseModel):
    # table name
    __tablename__ = 'user_hackers'
    # displayed fields
    visible = ['id', 'user_id', 'hacker_team_id', 'created_at', 'updated_at']

    # columns definitions
    id = db.Column(
        db.String, 
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
        nullable=False
    )
    hacker_team_id = db.Column(
        db.Integer,
        db.ForeignKey('hacker_teams.id'),
        nullable=False
    )
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()