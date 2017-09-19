from app.controllers.base_controller import BaseController
from app.services import speakerdocumentservice
from app.configs.constants import ROLE
from app.models import db
from app.models.speaker import Speaker
from app.models.speaker_document import SpeakerDocument


class SpeakerDocumentController(BaseController):

    @staticmethod
    def show(user):
        speaker = db.session.query(Speaker).filter_by(user_id=user['id']).first()
        if speaker is None:
            return BaseController.send_error_api(None, 'speaker not found')
        speaker = speaker.as_dict()
        _speaker_documents = speakerdocumentservice.show(speaker)
        if _speaker_documents['error']:
            return BaseController.send_error_api(_speaker_documents['data'], _speaker_documents['message'])
        return BaseController.send_response_api(_speaker_documents['data'], _speaker_documents['message'])

    @staticmethod
    def _show(speaker_id):
        speaker_documents = speakerdocumentservice.shows(speaker_id)
        if speaker_documents['error']:
            return BaseController.send_error_api(speaker_documents['data'], speaker_documents['message'])
        return BaseController.send_response_api(speaker_documents['data'], speaker_documents['message'])

    @staticmethod
    def view(id):
        speaker_documents = speakerdocumentservice.view(id)
        if speaker_documents is None:
            return BaseController.send_error_api(None, 'documents are not found')
        return BaseController.send_response_api(speaker_documents, 'documents retrieved succesfully')

    @staticmethod
    def create(request, user):
        if(user['role_id'] == ROLE['speaker']):            
            speaker = db.session.query(Speaker).filter_by(user_id=user['id']).first()
            if speaker is None:
                return BaseController.send_error_api(None, 'speaker not found')
            speaker = speaker.as_dict()
            speaker_id = speaker['id']
            document_data = request.files['document_data']            
            summary = request.form['summary'] if 'summary' in request.form else ''
            title = request.form['title'] if 'title' in request.form else ''
            is_used = request.form['is_used'] if 'is_used' in request.form else 0             
            if document_data and speaker_id:
                payloads = {
                    'document_data': document_data,
                    'speaker_id': speaker_id,
                    'title': title,
                    'summary': summary,
                    'is_used': is_used
                }
            else:
                return BaseController.send_error_api(None, 'field is not complete')
            result = speakerdocumentservice.create(payloads)
            if not result['error']:
                return BaseController.send_response_api(result['data'], result['message'])
            else:
                return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(None, 'Unauthorized user')
    
    @staticmethod
    def update(request, user, id):
        if(user['role_id'] == ROLE['speaker']):            
            speaker = db.session.query(Speaker).filter_by(user_id=user['id']).first()
            if speaker is None:
                return BaseController.send_error_api(None, 'speaker not found')
            speaker = speaker.as_dict()
            speaker_id = speaker['id']
            document_data = request.files['document_data']            
            summary = request.form['summary'] if 'summary' in request.form else ''
            title = request.form['title'] if 'title' in request.form else ''
            is_used = request.form['is_used'] if 'is_used' in request.form else 0             
            if document_data and speaker_id:
                payloads = {
                    'document_data': document_data,
                    'speaker_id': speaker_id,
                    'title': title,
                    'summary': summary,
                    'is_used': is_used
                }
            else:
                return BaseController.send_error_api(None, 'field is not complete')
            result = speakerdocumentservice.update(payloads, id)
            if not result['error']:
                return BaseController.send_response_api(result['data'], result['message'])
            else:
                return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(None, 'Unauthorized user')

    @staticmethod
    def admin_create(request, user):
        if(user['role_id'] == ROLE['admin']):            
            speaker_id = request.form['speaker_id'] if 'speaker_id' in request.form else None
            speaker = db.session.query(Speaker).filter_by(user_id=speaker_id).first()
            if speaker is None:
                return BaseController.send_error_api(None, request.form.to_dict())
            speaker = speaker.as_dict()
            speaker_id = speaker['id']
            document_data = request.files['document_data']
            summary = request.form['summary'] if 'summary' in request.form else ''
            title = request.form['title'] if 'title' in request.form else ''
            if document_data and speaker_id:
                payloads = {
                    'document_data': document_data,
                    'speaker_id': speaker_id,
                    'title': title,
                    'summary': summary
                }
            else:
                return BaseController.send_error_api(None, 'field is not complete')
            result = speakerdocumentservice.create(payloads)
            if not result['error']:
                return BaseController.send_response_api(result['data'], 'speaker document succesfully uploaded')
            else:
                return BaseController.send_error_api(None, result['data'])
        else:
            return BaseController.send_error_api(None, 'Unauthorized user')

    @staticmethod
    def delete(user, id):
        speaker_document = db.session.query(SpeakerDocument).filter_by(id=id).first()
        speaker = db.session.query(Speaker).filter_by(user_id=user['id']).first()
        if speaker_document and speaker is not None:
            speaker_document = speaker_document.as_dict()
            speaker = speaker.as_dict()
            if speaker_document['speaker_id'] == speaker['id']:
                speaker_document = speakerdocumentservice.delete(id)
                if speaker_document['error']:
                    return BaseController.send_response_api(None, 'speaker document not found')
                return BaseController.send_response_api(None, 'speaker document has been succesfully deleted')
            else:
                return BaseController.send_response_api(None, 'Unauthorized')
        else:
            return BaseController.send_response_api(None, 'speaker document not found or unauthorized')
