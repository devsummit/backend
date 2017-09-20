import datetime

from app.models import db
from app.models.base_model import BaseModel


class SpeakerCandidateLog(db.Model, BaseModel):
    # table name
    __tablename__ = 'speaker_candidate_logs'

    # visible fields
    visible = ['id', 'candidate_id', 'message', 'created_at', 'updated_at']

    # columns definitions
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey('speaker_candidates.id'),
        nullable=False
    )
    message = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
