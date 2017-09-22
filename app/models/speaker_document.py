import datetime
from app.models import db
from app.models.base_model import BaseModel


class SpeakerDocument(db.Model, BaseModel):
    __tablename__ = 'materials'

    visible = ['id', 'speaker_id', 'material', 'title', 'summary', 'is_used', 'created_at', 'updated_at']

    id = db.Column(db.Integer, primary_key=True)
    speaker_id = db.Column(
        db.Integer,
        db.ForeignKey('speakers.id'),
        nullable=False
    )
    speaker = db.relationship('Speaker')
    material = db.Column(db.String)
    title = db.Column(db.String)
    summary = db.Column(db.String)
    is_used = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
