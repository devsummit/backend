from flask import render_template, request
from app.controllers.base_controller import BaseController
from app.services import attendeeservice
from app.services import paymentservice
from app.services import ticketservice
from app.services import referalservice
from app.services import userservice
from app.services import boothservice
from app.services import speakerservice
from app.services import eventservice
from app.configs.constants import EVENTS_TYPE
from app.services import stageservice
from app.services import scheduleservice
from app.services import entrycashlogservice


class MainController(BaseController):
    def index():
        return render_template('admin/base/index.html')

    def getAttendees():
        attendees = attendeeservice.get(request)
        return render_template('admin/attendees/attendees.html', attendees=attendees['data'])

    def getPayments():
        payments = paymentservice.admin_get()
        return render_template('admin/payments/payments.html', payments=payments['data'])

    def getAuthorizePayments():
        param = {'transaction_status': 'authorize'}
        authorizepayments = paymentservice.admin_filter(param)
        return render_template('admin/payments/authorize-needed.html', payments=authorizepayments['data'])

    def getTickets():
        tickets = ticketservice.get()
        return render_template('admin/tickets/tickets.html', tickets=tickets)

    def getReferals():
        referals = referalservice.get()
        return render_template('admin/referals/referals.html', referals=referals)

    def getAccounts():
        accounts = userservice.list_user(request)
        return render_template('admin/accounts/accounts.html', accounts=accounts['data'])

    def getBooths():
        booths = boothservice.get(request)
        return render_template('admin/booths/booths.html', booths=booths['data'])

    def getSpeakers():
        speakers = speakerservice.get()
        return render_template('admin/speakers/speakers.html', speakers=speakers['data'])

    def getEvents():
        events = eventservice.index(request)
        return render_template('admin/events/events.html', events=events['data'], event_type=EVENTS_TYPE)

    def getStages():
        stages = stageservice.get()
        return render_template('admin/stages/stages.html', stages=stages)

    def getSchedules():
        schedules = scheduleservice.get()
        return render_template('admin/events/schedules/schedules.html', schedules=schedules['data'])

    def getEntryCashLogs():
        entrycashlogs = entrycashlogservice.get(request)
        return render_template('admin/entrycash/entrycash.html', entrycashlogs=entrycashlogs['data'])