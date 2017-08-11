import datetime

from app.models import db
from app.models.base_model import BaseModel
from app.models.stage import Stage


class StagePhotos(db.Model, BaseModel):

    # table name
    __tablename__ = 'stage_photos'
    # displayed fields
    visible = ['id', 'stage_id', 'url', 'created_at', 'updated_at']

    # columns definitions
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(
        db.String(40),
        db.ForeignKey('stages.id'),
        nullable=False
    )
    stage = db.relationship('Stage')
    url = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
