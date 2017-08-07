from flask import Blueprint, request


# import controller
from app.controllers.event_controller import EventController

events = Blueprint('events', __name__)

BASE = '/events'
@events.route(BASE, methods=['GET'])
def index():
	return EventController.index(request)


@events.route(BASE, methods=['PATCH'])
def edit():
	return EventController.edit(request)

