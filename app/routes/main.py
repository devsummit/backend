from flask import Blueprint, render_template, request
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


@main.route('/authorize-payments')
def getPaymentsAuthorize():
    return MainController.getAuthorizePayments()


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


@main.route('/speakers')
def get_speakers():
	return MainController.getSpeakers()


@main.route('/events')
def get_events():
    return MainController.getEvents()


@main.route('/stages')
def get_stages():
	return MainController.getStages()


@main.route('/schedules')
def schedules():
    return MainController.getSchedules()


@main.route('/partners', methods=['GET', 'POST'])
def partners():
    if(request.method == 'GET'):
        return MainController.getPartners()
    else:
        return MainController.createPartner(request)


@main.route('/entrycashlogs')
def entrycashlog():
    return MainController.getEntryCashLogs()

@main.route('/sponsors')
def sponsors():
    return MainController.getSponsors()
