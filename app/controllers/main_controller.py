from flask import render_template, request, redirect
from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import attendeeservice
from app.services import paymentservice
from app.services import ticketservice
from app.services import referalservice
from app.services import userservice
from app.services import boothservice
from app.services import speakerservice
from app.services import eventservice
from app.services import stageservice
from app.services import scheduleservice
from app.services import partnerservice
from app.services import entrycashlogservice
from app.services import sponsorservice
from app.services import rundownlistservice
from app.services import redeemcodeservice
from app.services import speakercandidateservice
from app.services import sourceservice
from app.services import orderservice
from app.services import overviewservice
from app.services import feedreportservice
from app.services import feedservice
from app.services import sponsortemplateservice
from app.services import invoiceservice
from app.services import packagemanagementservice
from app.services import tickettransferservice
from app.services import hackatonproposalservice
from app.configs.constants import ROLE
from app.controllers.partner_pj_controller import PartnerPjController

class MainController(BaseController):

    def login():
        return render_template('admin/auth/login.html', overview=overview)

    def index():
        attendees = overviewservice.getAttendees()
        users = overviewservice.getUsers()
        booths = overviewservice.getBooths()
        sponsors = overviewservice.getSponsors()
        finances = overviewservice.getFinances()
        order_count = overviewservice.getOrders()
        overview = {
            'users': users,
            'attendees': attendees,
            'booths': booths,
            'sponsors': sponsors,
            'finances': finances,
            'order': order_count
        }
        return render_template('admin/base/overview.html', overview=overview)

    def getAttendees():
        attendees = userservice.get_attendees()
        return render_template('admin/attendees/attendees.html', attendees=attendees['data'])


    def getPurchasedAttendees():
        purchased_attendees = userservice.get_purchased_attendees()
        return render_template('admin/attendees/purchased_attendees.html', attendees=purchased_attendees['data'])

    def getHackatonProposal():
        hackatonproposals = hackatonproposalservice.get_except('verified')
        return render_template('admin/accounts/hackaton_proposal.html', proposals=hackatonproposals['data'])

    def getPayments():
        param = {'transaction_status': 'captured'}
        payments = paymentservice.admin_filter(param)
        return render_template('admin/payments/payments.html', payments=payments['data'])

    def getAuthorizePayments():
        param = {'fraud_status': 'challenge'}
        authorizepayments = paymentservice.admin_filter(param)
        return render_template('admin/payments/authorize-needed.html', payments=authorizepayments['data'])

    def getTickets():
        tickets = ticketservice.get()
        return render_template('admin/tickets/tickets.html', tickets=tickets)

    def getReferals():
        referals = referalservice.get()
        partners = partnerservice.get(request)
        return render_template('admin/referals/referals.html', referals=referals, partners=partners)

    def admin_order():
        tickets = ticketservice.get()
        return render_template('admin/payments/admin_order.html', tickets=tickets['data'])


    def getAccounts():
        accounts = userservice.list_user(request)
        return render_template('admin/accounts/accounts.html', accounts=accounts['data'])

    def getHackers():
        hackers = userservice.list_hackaton_attendee()
        return render_template('admin/accounts/hackaton_users.html', hackers=hackers['data'])

    def getBooths():
        booths = boothservice.get(request)
        return render_template('admin/booths/booths.html', booths=booths['data'])

    def getSpeakers():
        speakers = speakerservice.get()
        return render_template('admin/speakers/speakers.html', speakers=speakers['data'])

    def getEvents():
        events = eventservice.index(request)
        return render_template('admin/events/events.html', events=events['data'])

    def getInvoice():
        invoices = invoiceservice.get()
        return render_template('admin/invoices/invoices.html', invoices=invoices['data'])

    def showInvoice(id):
        return render_template('admin/invoices/invoice-detail.html', invoice_id=id)

    def getStages():
        stages = stageservice.get()
        return render_template('admin/stages/stages.html', stages=stages)

    def getSchedules(request):
        schedules = {}
        if request.args.get('filter') is not None:
            filter = request.args.get('filter')
            schedules = scheduleservice.filter(filter)
        else:
            schedules = scheduleservice.get()

        return render_template('admin/events/schedules/schedules.html', schedules=schedules['data'])

    def getPartners():
        partners = partnerservice.get(request)
        return render_template('admin/partnership/partners/partners.html', partners=partners['data'])

    def getPartnersPj():
        partners = partnerservice.filter('community', request)
        users = userservice.get_user_filter(ROLE['user'])
        return render_template('admin/partnership/partners/partner_pj.html', partners=partners['data'], users=users)

    def getEntryCashLogs():
        entrycashlogs = entrycashlogservice.get(request)
        sources = sourceservice.get(request)
        return render_template('admin/entrycash/entrycash.html', entrycashlogs=entrycashlogs['data'], sources=sources['data'])

    def getSponsors():
        sponsors = sponsorservice.get(request)
        return render_template('admin/partnership/sponsors/sponsors.html', sponsors=sponsors['data'])

    def changepassword():
        return render_template('admin/users/changepassword.html')

    def getRundownList():
        rundownlist = rundownlistservice.get(request)
        return render_template('admin/rundown/rundown_list.html', rundownlist=rundownlist['data'])
        # return render_template('admin/rundown/rundown_list.html')

    def show_event_kanban():
        return render_template('admin/events/kanbans/kanban.html')

    def getRedeemCodes():
        redeemcodes = redeemcodeservice.get()
        return render_template('admin/redeem_codes/redeem_codes.html', redeemcodes=redeemcodes['data'])

    def showSpeakerCandidates():
        candidates = speakercandidateservice.get()
        return render_template('admin/speakers/speaker_candidates.html', candidates=candidates['data'])

    def getReportFinance(request):
        reportfinances = entrycashlogservice.get_by_filter(request)
        return render_template('admin/report_finance/report_finance.html', reportfinances=reportfinances['data'], total=reportfinances['included'])

    def getSource(request):
        sources = sourceservice.get(request)
        return render_template('admin/sources/source.html', sources=sources['data'])

    def getReportFeed(request):
        reportfeeds = feedreportservice.admin_get(request)
        return render_template('admin/feed_reports/feed_reports.html', reportfeeds=reportfeeds['data'])

    def getSponsorFeed(request):
        sponsors = sponsorservice.get(request)
        sponsortemplates = sponsortemplateservice.get(request)
        return render_template('admin/sponsor_template/sponsor_template.html', sponsors=sponsors['data'], sponsortemplates=sponsortemplates['data'])

    def getSponsorPost(request):
        sponsortemplates = sponsortemplateservice.get(request)
        return render_template('admin/communication/sponsor_post.html', sponsortemplates=sponsortemplates['data'])

    def getPackageManagement(request):
        packages = packagemanagementservice.get(request)
        return render_template('admin/partnership/packages/packages.html', packages=packages['data'])

    def getPackagePurchase(request):
        partners = partnerservice.filter('company', request)
        packages = packagemanagementservice.get(request)
        return render_template('admin/partnership/packages/package_purchase/package_purchase.html', partners=partners['data'], packages=packages['data'])

    def getTransferLog(request):
        logs = tickettransferservice.get_logs()
        return render_template('admin/ticket-transfer-log/ticket-transfer-log.html', logs=logs)

    def verification_list():
        return render_template('admin/payment_verification/verification_list.html')

    def admin_verification_list():
        orders = orderservice.unverified_order()
        return render_template('admin/payment_verification/admin_verification_list.html', orders=orders['data'])

    def submit_proof(request):
        return render_template('admin/payment_verification/submit_proof.html')


    def verify_email_address(token):
        result = userservice.email_address_verification(token)
        return render_template('admin/email_verification/email_verification.html', result=result)


    def reset_password_user(request):
        return render_template('admin/users/reset_password.html')


    def get_referal_info(id):
        referal_info = PartnerPjController.admin_get_info(id)
        return render_template('admin/referals/referal_details.html', referal_info=referal_info)

    def beacon_list():
        beacons =  [
            {
            "uuid": "775823475873240543758432",
            "description": "some description",
            "type": "booth",
            "type_id": 1,
            },
            {
            "uuid": "589234754237583472587348",
            "description": "some description 2",
            "type": "booth",
            "type_id": 2,
            }
        ]
        return render_template('admin/beacon/beacon.html', beacons=beacons)

    def beacon_show(id):
        beacon = {
            "uuid": "589234754237583472587348",
            "description": "some description 2",
            "type": "booth",
            "type_id": 2,
        }
        return render_template("admin/beacon/beacon_detail.html", beacon=beacon)
        
        
