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
        _speaker_documents = speakerdocumentservice.show(speaker['id'])
        if _speaker_documents is None:
            return BaseController.send_error_api(None, 'documents are not found')
        return BaseController.send_response_api(_speaker_documents, 'documents retrieved succesfully')

    @staticmethod
    def _show(speaker_id):
        speaker_documents = speakerdocumentservice.shows(speaker_id)
        if speaker_documents is None:
            return BaseController.send_error_api(None, 'documents are not found')
        return BaseController.send_response_api(speaker_documents, 'documents retrieved succesfully')

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
            if document_data and speaker_id:
                payloads = {
                    'document_data': document_data,
                    'speaker_id': speaker_id
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
    def admin_create(request, user):
        if(user['role_id'] == ROLE['admin']):
            speaker_id = request.form['speaker_id'] if 'speaker_id' in request.form else None
            speaker = db.session.query(Speaker).filter_by(user_id=speaker_id).first()
            if speaker is None:
                return BaseController.send_error_api(None, request.form.to_dict())
            speaker = speaker.as_dict()
            speaker_id = speaker['id']
            document_data = request.files['document_data']
            if document_data and speaker_id:
                payloads = {
                    'document_data': document_data,
                    'speaker_id': speaker_id
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
