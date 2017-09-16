from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, request  # noqa
import os
from app.services.helper import Helper 
# import model class
from app.models.speaker_document import SpeakerDocument
from app.models.base_model import BaseModel
from app.models.user import User
from app.builders.response_builder import ResponseBuilder


app = Flask(__name__)
# default saving, database saving and domain based url
app.config['POST_SPEAKER_DOC_DEST'] = 'app/static/documents/speakers/'
app.config['SAVE_SPEAKER_DOC_DEST'] = 'documents/speakers/'
app.config['GET_SPEAKER_DOC_DEST'] = 'static/'
app.config['STATIC_DEST'] = 'app/static/'
# These are the extentions that we are accepting to be upload
app.config['ALLOWED_SPEAKER_DOC_EXTENSIONS'] = set(['pdf', 'ppt'])


class SpeakerDocumentService():

    def show(self, speaker):
        response = ResponseBuilder()
        speaker_document = db.session.query(SpeakerDocument).filter_by(speaker_id=speaker['id']).all()
        if speaker_document is not None:
            speaker_document = BaseModel.as_list(speaker_document)
            for _speaker_document in speaker_document:
                _speaker_document['material'] = Helper().url_helper(_speaker_document['material'], app.config['GET_SPEAKER_DOC_DEST'])
                user = db.session.query(User).filter_by(id=speaker['user_id']).first().include_photos().as_dict()
                _speaker_document['user'] = user
            return response.set_data(speaker_document).build()
        else:
            data = 'data not found'
            return response.set_message(data).set_data(None).build()

    def shows(self, speaker_id):
        response = ResponseBuilder()
        speaker_document = db.session.query(SpeakerDocument).filter_by(speaker_id=speaker_id).all()
        if speaker_document is not None:
            speaker_document = BaseModel.as_list(speaker_document)
            for _speaker_document in speaker_document:
                _speaker_document['material'] = Helper().url_helper(_speaker_document['material'], app.config['GET_SPEAKER_DOC_DEST'])
            return response.set_data(_speaker_document).build()
        else:
            data = 'data not found'
            return response.set_data(None).set_message(data).build() 

    def view(self, id):
            speaker_document = db.session.query(SpeakerDocument).filter_by(id=id).first()
            if speaker_document is not None:
                speaker_document = speaker_document.as_dict()
                speaker_document['material'] = Helper().url_helper(speaker_document['material'], app.config['GET_SPEAKER_DOC_DEST'])
                return speaker_document
            else:
                data = 'data not found'
                return {
                    'error': True,
                    'data': data
                }   

    def create(self, payloads):
        response = ResponseBuilder()
        speaker_id = payloads['speaker_id']
        file = payloads['document_data']
        summary = payloads['summary']
        title = payloads['title']

        if file and Helper().allowed_file(file.filename, app.config['ALLOWED_SPEAKER_DOC_EXTENSIONS']):
            self.model_speaker_document = SpeakerDocument()
            db.session.add(self.model_speaker_document)
            try:
                file_name = Helper().time_string() + "_" + file.filename
                file.save(os.path.join(app.config['POST_SPEAKER_DOC_DEST'], file_name))
                self.model_speaker_document.material = app.config['SAVE_SPEAKER_DOC_DEST'] + file_name
                self.model_speaker_document.speaker_id = speaker_id
                self.model_speaker_document.summary = summary
                self.model_speaker_document.title = title
                db.session.commit()
                data = self.model_speaker_document.as_dict()
                data['material'] = Helper().url_helper(self.model_speaker_document.material, app.config['GET_SPEAKER_DOC_DEST'])
                return response.set_data(data).build()
            except SQLAlchemyError as e:
                data = e.orig.args
                return response.set_error(True).set_message(data).build()

    def delete(self, id):
        self.model_speaker_document = db.session.query(SpeakerDocument).filter_by(id=id)
        if self.model_speaker_document.first() is not None:
            # delete file
            os.remove(app.config['STATIC_DEST'] + self.model_speaker_document.first().material)
            # delete row
            self.model_speaker_document.delete()
            db.session.commit()
            return {
                'error': False,
                'data': None
            }
        else:
            data = 'data not found'
            return {
                'error': True,
                'data': data
            }   
