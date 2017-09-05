from flask import render_template
from app.controllers.base_controller import BaseController
from app.services import attendeeservice
from app.services import ticketservice
from app.services import referalservice
from app.services import boothservice


class MainController(BaseController):
    def index():
        return render_template('admin/base/index.html')

    def getAttendees():
        attendees = attendeeservice.get()
        return render_template('admin/attendees/attendees.html', attendees=attendees)

    def getTickets():
        tickets = ticketservice.get()
        return render_template('admin/tickets/tickets.html', tickets=tickets)

    def getReferals():
    	referals = referalservice.get()
    	return render_template('admin/referals/referals.html', referals=referals)

    def getBooths():
        booths = boothservice.get()
        return render_template('admin/booths/booths.html', booths=booths['data'])
