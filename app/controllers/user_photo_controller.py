from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import userphotoservice

class UserPhotoController(BaseController):

    @staticmethod
    def index():
        userPhotos = userphotoservice.get()
        return BaseController.send_response_api(userPhotos, 'photos retrieved succesfully')
    
    @staticmethod
    def show(user_id):
        userPhoto = userphotoservice.show(user_id)
        if userPhoto is None:
            return BaseController.send_error_api(None, 'photo not found')
        return BaseController.send_response_api(userPhoto, 'photo retrieved successfully')

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
            return BaseController.send_response_api(result['data'], 'user photo succesfully created')
        else:
            return BaseController.send_error_api(None, result['data'])

    
    @staticmethod
    def update(request, user_id):
        image_data = request.files
        if image_data and user_id:
            payloads = {
                'image_data': image_data,
                'user_id': user_id
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userphotoservice.update(payloads)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'user photo succesfully updated')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def delete(user_id):
        userPhoto = userphotoservice.delete(user_id)
        if userPhoto['error']:
            return BaseController.send_response_api(None, 'user photo not found')
        return BaseController.send_response_api(None, 'user photo for user id: ' + str(user_id) + ' has been succesfully deleted')