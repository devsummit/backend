import os
from werkzeug import secure_filename
import datetime
from app.models import db
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.services.helper import Helper 
from app.models.speaker import Speaker
from app.models.user_photo import UserPhoto


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
            if payloads['photo']:
                photo = self.save_file(payloads['photo'])
                userphoto = db.session.query(UserPhoto).filter_by(user_id=self.model_speaker.first().user_id)
                if userphoto.first():
                    userphoto.update({
                        'url': photo,
                        'updated_at': datetime.datetime.now()
                     })
                else:
                    userphoto = UserPhoto()
                    userphoto.user_id = self.model_speaker.first().user_id
                    userphoto.url = photo
                    db.session.add(userphoto)
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

    def save_file(self, file, id=None):
        if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                filename = secure_filename(file.filename)
                filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
                file.save(os.path.join(current_app.config['POST_PARTNER_PHOTO_DEST'], filename))
                if id:
                    temp_partner = db.session.query(Partner).filter_by(id=id).first()
                    partner_photo = temp_partner.as_dict() if temp_partner else None
                    if partner_photo is not None and partner_photo['photo'] is not None:
                        Helper().silent_remove(current_app.config['STATIC_DEST'] + partner_photo['photo'])
                return current_app.config['SAVE_PARTNER_PHOTO_DEST'] + filename
        else:
            return None
