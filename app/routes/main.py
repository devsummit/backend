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


@main.route('/events/kanban')
def event_kanban():
    return MainController.show_event_kanban()


@main.route('/stages')
def get_stages():
    return MainController.getStages()


@main.route('/schedules')
def schedules():
    return MainController.getSchedules(request)


@main.route('/adduserphoto')
def adduserphoto():
    return render_template('admin/users/user_photos_add.html')


@main.route('/partners', methods=['GET', 'POST'])
def partners():
    if(request.method == 'GET'):
        return MainController.getPartners()


@main.route('/entrycashlogs')
def entrycashlog():
    return MainController.getEntryCashLogs()


@main.route('/sponsors')
def sponsors():
    return MainController.getSponsors()


@main.route('/password')
def changepassword():
    return MainController.changepassword()


@main.route('/rundownlist')
def rundownlist():
    return MainController.getRundownList()


@main.route('/redeemcodes')
def redeemcodes():
    return MainController.getRedeemCodes()


@main.route('/speaker-candidates')
def speaker_candidates():
    return MainController.showSpeakerCandidates()


@main.route('/entrycashlogsfilter')
def report_finance_source():
    return MainController.getReportFinance(request)

@main.route('/notification')
def notification():
    return render_template('admin/communication/notification.html')

@main.route('/post')
def post():
    return render_template('admin/communication/post.html')

@main.route('/sources')
def source():
    return MainController.getSource(request)
