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
        self.model_candidate = db.session.query(
            SpeakerCandidate).filter_by(id=id).first()
        if self.model_candidate:
            return {
                'data': self.model_candidate.as_dict(),
                'message': 'candidate retrieved successfully',
                'error': False
            }
        else:
            return {
                'error': True,
                'data': 'candidate not found'
            }

    def update(self, payloads, id):
        self.model_candidate = db.session.query(
            SpeakerCandidate).filter_by(id=id)
        if self.model_candidate:
            new_data = payloads
            new_data['updated_at'] = datetime.datetime.now()
            self.model_candidate.update(new_data)
        else:
            return {
                'error': True,
                'data': "candidate not found"
            }

        try:
            db.session.commit()

            data = self.model_candidate.first()
            return {
                'error': False,
                'data': data.as_dict(),
                'included': []
            }
        except SQLAlchemyError as e:
            return {
                'error': True,
                'data': e.orig.args
            }

    def create(self, payloads):
        self.model_candidate = SpeakerCandidate()
        for key in payloads:
            setattr(self.model_candidate, key, payloads[key])
        db.session.add(self.model_candidate)
        try:
            db.session.commit()
            data = self.model_candidate.as_dict()
            return {
                'error': False,
                'data': data,
                'included': []
            }
        except SQLAlchemyError as e:
            return {
                'error': True,
                'data': e.orig.args
            }
