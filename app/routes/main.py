from flask import Blueprint, render_template
from app.controllers.main_controller import MainController


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return MainController.index()


@main.route('/attendees')
def get_attendees():
    return MainController.getAttendees()


@main.route('/payments')
def getPayments():
    return MainController.getPayments()


@main.route('/tickets')
def get_tickets():
    return MainController.getTickets()


@main.route('/referals')
def get_referals():
	return MainController.getReferals()


@main.route('/booths')
def get_booths():
	return MainController.getBooths()


@main.route('/login')
def login():
    return render_template('admin/auth/login.html')

@main.route('/accounts')
def get_accounts():
	return MainController.getAccounts()
