from flask import Blueprint, request


# import controller
from app.controllers.event_controller import EventController

events = Blueprint('events', __name__)


@events.route('/events', methods=['GET'])
def index():
	return EventController.index(request)


@events.route('/events', methods=['PATCH'])
def edit():
	return EventController.edit(request)

