'''
put api route in here
'''
from flask import Blueprint, request

# import middlewares
from app.middlewares.authentication import token_required

# controllers import
from app.controllers.event_controller import EventController

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
@token_required
def api_index(*args, **kwargs):
	return 'api index'


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
