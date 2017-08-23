from flask import render_template, request
from app.controllers.base_controller import BaseController
from app.services import attendeeservice
import requests


class MainController(BaseController):
    def index():
        return render_template('admin/base/index.html')

    def getAttendees():
        attendees = attendeeservice.get()
        return render_template('admin/attendees.html', attendees=attendees)
