'''
put api route in here
'''
from flask import Blueprint, request

# import middlewares
from app.middlewares.authentication import token_required

# controllers import
from app.controllers.ticket_controller import TicketController

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
@token_required
def api_index(*args, **kwargs):
	return 'api index'

# Ticket api
# Fetch ticket list
@api.route('/tickets', methods=['GET', 'POST'])
@token_required
def ticket_get(*args, **kwargs):
	if(request.method == 'POST'):
		return TicketController.create(request)
	elif(request.method == 'GET'):
		return TicketController.index()

# Get ticket by id
@api.route('/tickets/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def ticket_show(id, *args, **kwargs):
	if(request.method == 'PUT' or request.method == 'PATCH'):
		return TicketController.update(request, id)
	elif(request.method == 'DELETE'):
		return TicketController.delete(id)
	elif(request.method == 'GET'):
		return TicketController.show(id)