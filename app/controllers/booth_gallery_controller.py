from app.controllers.base_controller import BaseController
from app.services import boothgalleryservice

from app.models import db
from app.models.booth import Booth
from app.models.booth_gallery import BoothGallery


class BoothGalleryController(BaseController):

    @staticmethod
    def index():
        result = boothgalleryservice.index()
        print("RESULT", result)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def show(id):
        result = boothgalleryservice.show(id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])
        
    @staticmethod
    def self_gallery(user):
        booth = db.session.query(Booth).filter_by(user_id=user['id'])
        if booth.first() is not None:
            booth_id = booth.first().as_dict()['id']

        print(booth_id)
        result = boothgalleryservice.self_gallery(booth_id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def booth_gallery(booth_id):
        result = boothgalleryservice.self_gallery(booth_id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def create(request, user):
        booth = db.session.query(Booth).filter_by(user_id=user['id'])
        if booth.first() is not None:
            booth_id = booth.first().as_dict()['id']
        files = request.files.getlist("image_files")

        if booth_id and files:
            payloads = {
                'booth_id': booth_id,
                'image_files': files 
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = boothgalleryservice.create(payloads)
        if not result['error']:
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(result['data'], result['message'])

    @staticmethod
    def delete(id):
        result = boothgalleryservice.delete(id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])


