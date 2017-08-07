from flask import Blueprint, request


# import controller
from app.controllers.event_controller import EventController

events = Blueprint('events', __name__)

@events.route('/', methods=['GET'])
def index():
	return EventController.index()

@events.route('/<event_id>', methods=['GET'])
def show(event_id):
	return EventController.show(event_id)

@events.route('', methods=['POST'])
def create():
	return EventController.create(request)

@events.route('/<event_id>', methods=['PATCH'])
def update(event_id):
	return EventController.update(request, event_id)

@events.route('/<event_id>', methods=['DELETE'])
def delete(event_id):
	return EventController.delete(event_id)

