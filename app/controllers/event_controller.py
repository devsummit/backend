# parent class imports
from app.controllers.base_controller import BaseController
from app.services import eventservice


class EventController(BaseController):

        @staticmethod
        def index(request):
                return BaseController.send_response_api({'index': 'this is index'})


        @staticmethod
        def edit(request):
                return BaseController.send_response_api({'index': 'this is edit'})