import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.speaker import Speaker


class SpeakerService():

    def get(self):
        speakers = db.session.query(Speaker).all()
        # add includes
        included = self.get_includes(speakers)
        return {
            'data': speakers,
            'included': included
        }

    def show(self, id):
        speaker = db.session.query(Speaker).filter_by(id=id).first()
        included = self.get_includes(speaker)
        return {
            'data': speaker,
            'included': included
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
