from app.controllers.base_controller import BaseController
from app.services import speakerservice


class SpeakerController(BaseController):

    @staticmethod
    def index():
        speakers = speakerservice.get()
        return BaseController.send_response_api(
            speakers['data'],
            speakers['message'] 
        )

    @staticmethod
    def show(id):
        speaker = speakerservice.show(id)
        if speaker['error']:
            return BaseController.send_error_api(
                speaker['data'],
                speaker['message']
            )
        return BaseController.send_response_api(
            speaker['data'], 
            speaker['message']
        )

    @staticmethod
    def update(request, id):
        user_id = request.form['user_id'] if 'user_id' in request.form else None
        job = request.form['job'] if 'job' in request.form else None
        summary = request.form['summary'] if 'summary' in request.form else None
        information = request.form['information'] if 'information' in request.form else None
        photo = request.files['photo'] if 'photo' in request.files else None

        if user_id and job and summary and information:
            payloads = {
                'user_id': user_id,
                'job': job,
                'summary': summary,
                'information': information,
                'photo': photo
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
