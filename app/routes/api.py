'''
put api route in here
'''
from flask import Blueprint, request

# import middlewares
from app.middlewares.authentication import token_required

# controllers import
from app.controllers.ticket_controller import TicketController
from app.controllers.stage_controller import StageController
from app.controllers.beacon_controller import BeaconController
from app.controllers.spot_controller import SpotController
from app.controllers.order_controller import OrderController
from app.controllers.order_details_controller import OrderDetailsController
from app.controllers.event_controller import EventController
from app.controllers.schedule_controller import ScheduleController
from app.controllers.points_controller import PointsController
from app.controllers.ticket_transfer_controller import TicketTransferController

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
@token_required
def api_index(*args, **kwargs):
	return 'api index'


# Ticket api


@api.route('/tickets', methods=['GET', 'POST'])
@token_required
def ticket(*args, **kwargs):
	if(request.method == 'POST'):
		return TicketController.create(request)
	elif(request.method == 'GET'):
		return TicketController.index()

# Ticket route by id


@api.route('/tickets/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def ticket_id(id, *args, **kwargs):
	if(request.method == 'PUT' or request.method == 'PATCH'):
		return TicketController.update(request, id)
	elif(request.method == 'DELETE'):
		return TicketController.delete(id)
	elif(request.method == 'GET'):
		return TicketController.show(id)

# Stage api


@api.route('/stages', methods=['GET', 'POST'])
@token_required
def stage(*args, **kwargs):
	if(request.method == 'POST'):
		return StageController.create(request)
	elif(request.method == 'GET'):
		return StageController.index()

# Stage route by id


@api.route('/stages/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def stage_id(id, *args, **kwargs):
	if(request.method == 'PUT' or request.method == 'PATCH'):
		return StageController.update(request, id)
	elif(request.method == 'DELETE'):
		return StageController.delete(id)
	elif(request.method == 'GET'):
		return StageController.show(id)

# Beacon api


@api.route('/beacons', methods=['GET', 'POST'])
@token_required
def beacon(*args, **kwargs):
	if(request.method == 'POST'):
		return BeaconController.create(request)
	elif(request.method == 'GET'):
		return BeaconController.index()

# Beacon route by id


@api.route('/beacons/<id>', methods=['PUT', 'PATCH', 'DELETE'])
@token_required
def beacon_id(id, *args, **kwargs):
	if(request.method == 'PUT' or request.method == 'PATCH'):
		return BeaconController.update(request, id)
	elif(request.method == 'DELETE'):
		return BeaconController.delete(id)

# Spot api


@api.route('/spots', methods=['GET'])
@token_required
def spot(*args, **kwargs):
	return SpotController.index()

# Spot route by id


@api.route('/spots/<id>', methods=['PUT', 'PATCH'])
@token_required
def spot_id(id, *args, **kwargs):
	return SpotController.update(request, id)


# Ticket Order API

@api.route('/orders', methods=['GET', 'POST'])
@token_required
def orders(*args, **kwargs):
	user_id = kwargs['user'].id
	if(request.method == 'GET'):
		return OrderController.index()
	elif(request.method == 'POST'):
		return OrderController.create(request, user_id)


@api.route('/orders/<id>', methods=['DELETE', 'GET'])
@token_required
def orders_id(id, *args, **kwargs):
	if(request.method == 'GET'):
		return OrderController.show(id)
	elif(request.method == 'DELETE'):
		return OrderController.delete(id)


@api.route('/orders/<order_id>/details', methods=['GET', 'POST'])
@token_required
def orders_details(order_id, *args, **kwargs):
	if(request.method == 'GET'):
		return OrderDetailsController.index(order_id)
	elif(request.method == 'POST'):
		return OrderDetailsController.create(order_id, request)


@api.route('/orders/<order_id>/details/<detail_id>', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
@token_required
def orders_details_id(order_id, detail_id, *args, **kwargs):
	if(request.method == 'GET'):
		return OrderDetailsController.show(order_id, detail_id)
	elif(request.method == 'PUT' or request.method == 'PATCH'):
		return OrderDetailsController.update(detail_id, request)
	elif(request.method == 'DELETE'):
		return OrderDetailsController.delete(order_id, detail_id)

# Events API


@api.route('/events', methods=['GET'])
def index():
	return EventController.index()


@api.route('/events/<event_id>', methods=['GET'])
def show(event_id):
	return EventController.show(event_id)


@api.route('/events', methods=['POST'])
def create():
	return EventController.create(request)


@api.route('/events/<event_id>', methods=['PATCH'])
def update(event_id):
	return EventController.update(request, event_id)


@api.route('/events/<event_id>', methods=['DELETE'])
def delete(event_id):
	return EventController.delete(event_id)


# Schedule api


@api.route('/schedules', methods=['GET', 'POST'])
@token_required
def schedule(*args, **kwargs):
	if(request.method == 'POST'):
		return ScheduleController.create(request)
	elif(request.method == 'GET'):
		return ScheduleController.index()

# Beacon route by id


@api.route('/schedules/<id>', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
@token_required
def schedule_id(id, *args, **kwargs):
	if(request.method == 'PUT' or request.method == 'PATCH'):
		return ScheduleController.update(request, id)
	elif(request.method == 'GET'):
		return ScheduleController.show(id)
	elif(request.method == 'DELETE'):
		return ScheduleController.delete(id)

# Point endpoint


@api.route('/points/transfer', methods=['POST'])
@token_required
def transfer_points(*args, **kwargs):
	user = kwargs['user'].as_dict()
	if(user['role_id'] == 1 or user['role_id'] == 3):
		return PointsController.transfer_point(request, user['id'])
	return 'You cannot transfer points'


@api.route('/points/logs', methods=['GET'])
@token_required
def transfer_points_log(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return PointsController.transfer_point_log(request, user)


# Ticket Transfer endpoint

@api.route('/tickets/transfer/logs', methods=['GET'])
@token_required
def ticket_transfer_logs(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return TicketTransferController.ticket_transfer_logs(user)


@api.route('/tickets/transfer', methods=['POST'])
@token_required
def ticket_transfer(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return TicketTransferController.ticket_transfer(request, user)