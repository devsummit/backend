from app.controllers.base_controller import BaseController
from app.services import rundownlistservice


class RundownListController(BaseController):

	@staticmethod
	def index():
		rundownlist = rundownlistservice.get()
		if rundownlist['error']:
			return BaseController.send_error_api(rundownlist['data'], rundownlist['message'])
		return BaseController.send_response_api(rundownlist['data'], rundownlist['message'], rundownlist['included'])
		
	@staticmethod
	def create(request):
		stage_id = request.json['stage_id'] if 'stage_id' in request.json else None
		event_id = request.json['event_id'] if 'event_id' in request.json else None
		time_start = request.json['time_start'] if 'time_start' in request.json else None
		time_end = request.json['time_end'] if 'time_end' in request.json else None

		if stage_id and event_id and time_start and time_end:
			payloads = {
				'stage_id': stage_id,
				'event_id': event_id,
				'time_start': time_start,
				'time_end': time_end
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = scheduleservice.create(payloads)
		if not result['error']:
			return BaseController.send_response_api(result['data'], 'schedule succesfully created', result['included'])
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def update(request, id):
		stage_id = request.json['stage_id'] if 'stage_id' in request.json else None
		event_id = request.json['event_id'] if 'event_id' in request.json else None
		time_start = request.json['time_start'] if 'time_start' in request.json else None
		time_end = request.json['time_end'] if 'time_end' in request.json else None
		if stage_id and event_id and time_start and time_end:
			payloads = {
				'stage_id': stage_id,
				'event_id': event_id,
				'time_start': time_start,
				'time_end': time_end
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = scheduleservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'schedule succesfully updated', result['included'])
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(id):
		schedule = scheduleservice.delete(id)
		if schedule['error']:
			return BaseController.send_response_api(None, 'schedule not found')
		return BaseController.send_response_api(None, 'schedule has been succesfully deleted')