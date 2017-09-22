from flask import current_app

import datetime

# import classes
from app.models import db
from app.models.base_model import BaseModel
from app.services.helper import Helper


class SpeakerCandidate(db.Model, BaseModel):
    # table name
    __tablename__ = 'speaker_candidates'
    # displayed fields
    visible = ['id', 'first_name', 'last_name', 'email',
               'job', 'stage', 'summary',  'created_at', 'updated_at']

    # columns definitions
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, index=True, unique=True)
    job = db.Column(db.String)
    summary = db.Column(db.String)
    stage = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
