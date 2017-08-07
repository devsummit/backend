# parent class imports
from app.controllers.base_controller import BaseController
from app.services import eventservice
from app.models.events import Events


class EventController(BaseController):

        @staticmethod
        def index():
                result = eventservice.index()
                return BaseController.send_response_api(result, 'events retrieved successfully')


        @staticmethod
        def show(id):
                result = eventservice.show(id)
                return BaseController.send_response_api(result, 'event retrieved succesfully')

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