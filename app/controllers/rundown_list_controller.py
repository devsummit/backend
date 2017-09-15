from app.controllers.base_controller import BaseController
from app.services import rundownlistservice


class RundownListController(BaseController):

    @staticmethod
    def get(request):
        rundownlist = rundownlistservice.get(request)
        if rundownlist['error']:
            return BaseController.send_error_api(rundownlist['data'], rundownlist['message'])
        return BaseController.send_response_api(rundownlist['data'], rundownlist['message'], rundownlist['included'])

    @staticmethod
    def create(request):
        description = request.json['description'] if 'description' in request.json else None
        location = request.json['location'] if 'location' in request.json else None
        time_start = request.json['time_start'] if 'time_start' in request.json else None
        time_end = request.json['time_end'] if 'time_end' in request.json else None

        if description and location and time_start and time_end:
            payloads = {
                'description': description,
                'time_start': time_start,
                'time_end': time_end,
                'location': location
            }
            result = rundownlistservice.create(payloads)
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'rundown succesfully created', result['included'])
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def update(request, id):
        description = request.json['description'] if 'description' in request.json else None
        location = request.json['location'] if 'location' in request.json else None
        time_start = request.json['time_start'] if 'time_start' in request.json else None
        time_end = request.json['time_end'] if 'time_end' in request.json else None

        if description and location and time_start and time_end:
            payloads = {
                'description': description,
                'time_start': time_start,
                'time_end': time_end,
                'location': location
            }
            result = rundownlistservice.update(payloads, id)
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'rundown succesfully updated', result['included'])
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def show(id):
        rundown = rundownlistservice.show(id)
        if rundown['error']:
            return BaseController.send_error_api(rundown['data'], rundown['message'])
        return BaseController.send_response_api(rundown['data'], rundown['message'], rundown['included'])

    @staticmethod
    def delete(id):
        rundown = rundownlistservice.delete(id)
        if rundown['error']:
            return BaseController.send_response_api(None, 'rundown not found')
        return BaseController.send_response_api(None, 'rundown has been succesfully deleted')
