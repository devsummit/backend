import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.speaker_candidate import SpeakerCandidate


class SpeakerCandidateService():

    def get(self):
        candidates = db.session.query(SpeakerCandidate).all()
        _candidates = []
        for candidate in candidates:
            data = candidate.as_dict()
            _candidates.append(data)
        return {
            'data': _candidates,
            'message': 'speaker candidate retrieved successfully',
            'error': False
        }

    def show(self, id):
        pass

    def update(self, payloads, id):
        pass

