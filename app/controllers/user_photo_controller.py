from app.controllers.base_controller import BaseController
from app.services import userphotoservice


class UserPhotoController(BaseController):

    @staticmethod
    def index():
        user_photos = userphotoservice.get()
        if user_photos is None:
            return BaseController.send_error_api(None, 'photo not found')
        return BaseController.send_response_api(user_photos, 'photos retrieved succesfully')

    @staticmethod
    def show(user_id):
        user_photo = userphotoservice.show(user_id)
        if user_photo['error']:
            return BaseController.send_error_api(user_photo['data'], user_photo['message'])
        return BaseController.send_response_api(user_photo['data'], user_photo['message'])

    @staticmethod 
    def create(request, user_id):
        image_data = request.files['image_data']
        if image_data and user_id:
            payloads = {
                'image_data': image_data,
                'user_id': user_id
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userphotoservice.create(payloads)
        if not result['error']:
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(result['data'], result['message'])

    @staticmethod
    def delete(user_id):
        user_photo = userphotoservice.delete(user_id)
        if user_photo['error']:
            return BaseController.send_response_api(None, 'user photo not found')
        return BaseController.send_response_api(None, 'user photo for user id: ' + str(user_id) + ' has been succesfully deleted')
