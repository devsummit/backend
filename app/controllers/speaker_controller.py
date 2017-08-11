from app.models.base_model import BaseModel
from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import speakerservice

class SpeakerController(BaseController):

    @staticmethod
    def index():
        speakers = speakerservice.get()
        return BaseController.send_response_api(
            BaseModel.as_list(speakers['data']), 
            'speakers retrieved succesfully', 
            speakers['included']
        )

    @staticmethod
    def show(id):
        speaker = speakerservice.show(id)
        return BaseController.send_response_api(
            speaker['data'].as_dict(), 
            'speaker retrieved succesfully', 
            speaker['included']
        )

    @staticmethod
    def update(request, id):
        user_id = request.json['user_id'] if 'user_id' in request.json else None
        job = request.json['job'] if 'job' in request.json else None
        summary = request.json['summary'] if 'summary' in request.json else None
        information = request.json['information'] if 'information' in request.json else None

        if user_id and job and summary and information:
            payloads = {
                'user_id': user_id,
                'job': job,
                'summary': summary,
                'information': information
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = speakerservice.update(payloads, id)

        if not result['error']:
            return BaseController.send_response_api(
                result['data'], 
                'speaker succesfully updated', 
                result['included']
            )
        else:
            return BaseController.send_error_api(None, result['data'])