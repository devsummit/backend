from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import ticketservice


class TicketController(BaseController):

	@staticmethod
	def index():
		tickets = ticketservice.get()
		return BaseController.send_response_api(BaseModel.as_list(tickets), 'tickets retrieved successfully')

	@staticmethod
	def show(id):
		ticket = ticketservice.show(id)
		if ticket is None:
			return BaseController.send_error_api(None, 'ticket not found')
		return BaseController.send_response_api(ticket.as_dict(), 'ticket retrieved successfully')

	@staticmethod
	def create(request):
		ticket_type = request.json['ticket_type'] if 'ticket_type' in request.json else None
		price = request.json['price'] if 'price' in request.json else None
		information = request.json['information'] if 'information' in request.json else ''

		if ticket_type and price:
			payloads = {
				'ticket_type': ticket_type,
				'price': price,
				'information': information
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = ticketservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'ticket succesfully created')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def update(request, id):
		ticket_type = request.json['ticket_type'] if 'ticket_type' in request.json else None
		price = request.json['price'] if 'price' in request.json else None
		information = request.json['information'] if 'information' in request.json else ''
		if ticket_type and price:
			payloads = {
				'ticket_type': ticket_type,
				'price': price,
				'information': information
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = ticketservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'ticket succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])		

	@staticmethod
	def delete(id):
		ticket = ticketservice.delete(id)
		if ticket['error']:
			return BaseController.send_response_api(None, 'ticket not found')
		return BaseController.send_response_api(None, 'ticket with id: ' + id + ' has been succesfully deleted')
