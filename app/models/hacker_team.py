import datetime

from app.models.base_model import BaseModel
from app.models import db


class HackerTeam(db.Model, BaseModel):
    # table name
    __tablename__ = 'hacker_teams'
    # displayed fields
    visible = ['id', 'name', 'logo', 'project_name', 'project_url', 'theme', 'created_at', 'updated_at', 'ticket_id']

    # columns definitions
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    name = db.Column(
        db.String(60),
        nullable=False
    )
    logo = db.Column(db.String(180))
    project_name = db.Column(db.String(60))
    project_url = db.Column(db.String(250))
    theme = db.Column(db.String(60))
    ticket_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()