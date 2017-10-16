from app.controllers.base_controller import BaseController
from app.services import ticketservice


class TicketController(BaseController):

	@staticmethod
	def index():
		tickets = ticketservice.get()
		return BaseController.send_response_api(tickets['data'], tickets['message'])

	@staticmethod
	def show(id):
		ticket = ticketservice.show(id)
		if ticket is None:
			return BaseController.send_error_api(None, 'ticket not found')
		return BaseController.send_response_api(ticket, 'ticket retrieved successfully')

	@staticmethod
	def create(request):
		ticket_type = request.form['ticket_type'] if 'ticket_type' in request.form else None
		price = request.form['price'] if 'price' in request.form else None
		information = request.form['information'] if 'information' in request.form else ''
		type = request.form['type'] if 'type' in request.form else ''
		proposal_url = request.files['proposal_url'] if 'proposal_url' in request.files else None
		usd_price = request.form['usd_price'] if 'usd_price' in request.form else None

		if ticket_type and price:
			payloads = {
				'ticket_type': ticket_type,
				'price': price,
				'information': information,
				'type': type,
				'proposal_url': proposal_url,
				'usd_price': usd_price
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
		ticket_type = request.form['ticket_type'] if 'ticket_type' in request.form else None
		price = request.form['price'] if 'price' in request.form else None
		information = request.form['information'] if 'information' in request.form else ''
		type = request.form['type'] if 'type' in request.form else ''
		proposal_url = request.files['proposal_url'] if 'proposal_url' in request.files else None
		usd_price = request.form['usd_price'] if 'usd_price' in request.form else None

		if ticket_type and price:
			payloads = {
				'ticket_type': ticket_type,
				'price': price,
				'information': information,
				'type': type,
				'proposal_url': proposal_url,
				'usd_price': usd_price
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
