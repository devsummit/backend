# parent class imports
from app.controllers.base_controller import BaseController
from app.services import eventservice


class EventController(BaseController):

        @staticmethod
        def index():
                result = eventservice.index()
                if result['error']:
                        return BaseController.send_error_api(result['data'], result['message'])
                return BaseController.send_response_api(result['data'], result['message'])

        @staticmethod
        def show(id):
                result = eventservice.show(id)
                if result['error']:
                        return BaseController.send_error_api(result['data'], result['message'])
                return BaseController.send_response_api(result['data'], result['message'])

        @staticmethod
        def create(request):
                payloads = request.json['data']
                result = eventservice.create(payloads)
                return BaseController.send_response_api(result['data'], 'event created succesfully')

        @staticmethod
        def update(request, id):
                payloads = request.json['data']
                result = eventservice.update(id, payloads)
                return BaseController.send_response_api(result['data'], 'event updated succesfully')

        @staticmethod
        def delete(id):
                result = eventservice.delete(id)
                return BaseController.send_response_api(result['data'], 'event deleted succesfully')
