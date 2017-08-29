import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.speaker import Speaker


class SpeakerService():

    def get(self):
        speakers = db.session.query(Speaker).all()
        _speakers = []
        for speaker in speakers:
            data = speaker.as_dict()
            data['user'] = speaker.user.include_photos().as_dict()
            _speakers.append(data)
        return {
            'data': _speakers,
            'message': 'speaker retrieved successfully',
            'error': False
        }

    def show(self, id):
        speaker = db.session.query(Speaker).filter_by(id=id).first()
        if speaker is None:
            data = {
                'user_exist': True
            }
            return {
                'data': data,
                'error': True,
                'message': 'speaker not found'
            }
        data = speaker.as_dict()
        data['user'] = speaker.user.include_photos().as_dict()
        return {
            'error': False,
            'data': data,
            'message': 'speaker retrieved'
        }

    def update(self, payloads, id):
        try:
            self.model_speaker = db.session.query(Speaker).filter_by(id=id)
            self.model_speaker.update({
                'job': payloads['job'],
                'summary': payloads['summary'],
                'information': payloads['information'],
                'updated_at': datetime.datetime.now()
            })
            db.session.commit()
            data = self.model_speaker.first()
            included = self.get_includes(data)
            return {
                'error': False,
                'data': data.as_dict(),
                'included': included
            }
        except SQLAlchemyError as e:
            data = e.orig.args
            return {
                'error': True,
                'data': data
            }

    def get_includes(self, speakers):
        included = []
        if isinstance(speakers, list):
            for speaker in speakers:
                temp = {}
                temp['user'] = speaker.user.as_dict()
                included.append(temp)
        else:
            temp = {}
            temp['user'] = speakers.user.as_dict()
            included.append(temp)
        return included
