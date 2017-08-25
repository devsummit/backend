from flask import render_template
from app.controllers.base_controller import BaseController
from app.services import attendeeservice
from app.services import paymentservice


class MainController(BaseController):
    def index():
        return render_template('admin/base/index.html')

    def getAttendees():
        attendees = attendeeservice.get()
        return render_template('admin/attendees/attendees.html', attendees=attendees)
    
    def getPayments():
        payments = paymentservice.get()
        return render_template('admin/payments/payments.html', payments=payments)
