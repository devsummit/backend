'''
put api route in here
'''
from flask import Blueprint, request

# import middlewares
from app.middlewares.authentication import token_required

# controllers import
from app.controllers.ticket_controller import TicketController
from app.controllers.stage_controller import StageController
from app.controllers.beacon_controller import BeaconController
from app.controllers.spot_controller import SpotController
from app.controllers.order_controller import OrderController
from app.controllers.order_details_controller import OrderDetailsController
from app.controllers.event_controller import EventController
from app.controllers.schedule_controller import ScheduleController
from app.controllers.points_controller import PointsController
from app.controllers.user_photo_controller import UserPhotoController
from app.controllers.speaker_controller import SpeakerController
from app.controllers.ticket_transfer_controller import TicketTransferController
from app.controllers.speaker_document_controller import SpeakerDocumentController
from app.controllers.newsletter_controller import NewsletterController
from app.controllers.booth_controller import BoothController
from app.controllers.user_ticket_controller import UserTicketController
from app.controllers.attendee_controller import AttendeeController
from app.controllers.payment_controller import PaymentController
from app.controllers.referal_controller import ReferalController
from app.controllers.user_controller import UserController
from app.controllers.partner_controller import PartnerController
from app.controllers.entry_cash_log_controller import EntryCashLogController
from app.controllers.sponsor_controller import SponsorController
from app.controllers.rundown_list_controller import RundownListController
from app.configs.constants import ROLE


api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
@token_required
def api_index(*args, **kwargs):
    return 'api index'


# Ticket api


@api.route('/tickets', methods=['GET', 'POST'])
@token_required
def ticket(*args, **kwargs):
    if(request.method == 'POST'):
        return TicketController.create(request)
    elif(request.method == 'GET'):
        return TicketController.index()

# Ticket route by id


@api.route('/tickets/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def ticket_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return TicketController.update(request, id)
    elif(request.method == 'DELETE'):
        return TicketController.delete(id)
    elif(request.method == 'GET'):
        return TicketController.show(id)

# Stage api


@api.route('/stages', methods=['GET', 'POST'])
@token_required
def stage(*args, **kwargs):
    if(request.method == 'POST'):
        return StageController.create(request)
    elif(request.method == 'GET'):
        return StageController.index()

# Stage route by id


@api.route('/stages/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def stage_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return StageController.update(request, id)
    elif(request.method == 'DELETE'):
        return StageController.delete(id)
    elif(request.method == 'GET'):
        return StageController.show(id)

# Stage Picture api


@api.route('/stages/<stage_id>/pictures', methods=['GET', 'POST'])
@token_required
def stage_picture(stage_id, *args, **kwargs):
    if(request.method == 'POST'):
        return StageController.createPicture(request, stage_id)
    elif(request.method == 'GET'):
        return StageController.indexPicture(stage_id)

# Stage Picture route by id


@api.route('/stages/<stage_id>/pictures/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def stage_picture_id(stage_id, id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return StageController.updatePicture(request, stage_id, id)
    elif(request.method == 'DELETE'):
        return StageController.deletePicture(stage_id, id)
    elif(request.method == 'GET'):
        return StageController.showPicture(stage_id, id)

# Beacon api


@api.route('/beacons', methods=['GET', 'POST'])
@token_required
def beacon(*args, **kwargs):
    if(request.method == 'POST'):
        return BeaconController.create(request)
    elif(request.method == 'GET'):
        return BeaconController.index()

# Beacon route by id


@api.route('/beacons/<id>', methods=['PUT', 'PATCH', 'DELETE'])
@token_required
def beacon_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return BeaconController.update(request, id)
    elif(request.method == 'DELETE'):
        return BeaconController.delete(id)

# Spot api


@api.route('/spots', methods=['GET'])
@token_required
def spot(*args, **kwargs):
    return SpotController.index()

# Spot route by id


@api.route('/spots/<id>', methods=['PUT', 'PATCH'])
@token_required
def spot_id(id, *args, **kwargs):
    return SpotController.update(request, id)


# Ticket Order API

@api.route('/orders', methods=['GET', 'POST'])
@token_required
def orders(*args, **kwargs):
    user_id = kwargs['user'].id
    if(request.method == 'GET'):
        return OrderController.index(user_id)
    elif(request.method == 'POST'):
        return OrderController.create(request, user_id)


@api.route('/orders/<id>', methods=['DELETE', 'GET'])
@token_required
def orders_id(id, *args, **kwargs):
    if(request.method == 'GET'):
        return OrderController.show(id)
    elif(request.method == 'DELETE'):
        return OrderController.delete(id)


@api.route('/orders/<order_id>/details', methods=['GET', 'POST'])
@token_required
def orders_details(order_id, *args, **kwargs):
    if(request.method == 'GET'):
        return OrderDetailsController.index(order_id)
    elif(request.method == 'POST'):
        return OrderDetailsController.create(order_id, request)


@api.route('/orders/<order_id>/details/<detail_id>', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
@token_required
def orders_details_id(order_id, detail_id, *args, **kwargs):
    if(request.method == 'GET'):
        return OrderDetailsController.show(order_id, detail_id)
    elif(request.method == 'PUT' or request.method == 'PATCH'):
        return OrderDetailsController.update(detail_id, request)
    elif(request.method == 'DELETE'):
        return OrderDetailsController.delete(order_id, detail_id)

# Events API


@api.route('/events', methods=['GET'])
def index():
    return EventController.index(request)


@api.route('/events/<event_id>', methods=['GET'])
def show(event_id):
    return EventController.show(event_id)


@api.route('/events', methods=['POST'])
def create():
    return EventController.create(request)


@api.route('/events/<event_id>', methods=['PATCH', 'PUT'])
def update(event_id):
    return EventController.update(request, event_id)


@api.route('/events/<event_id>', methods=['DELETE'])
def delete(event_id):
    return EventController.delete(event_id)


# Schedule api


@api.route('/schedules', methods=['GET', 'POST'])
@token_required
def schedule(*args, **kwargs):
	filter = request.args.get('filter')
	day = request.args.get('day')
	if(request.method == 'POST'):
		return ScheduleController.create(request)
	elif(request.method == 'GET' and filter is None and day is None):
		return ScheduleController.index()
	elif(request.method == 'GET' and filter is not None):
		return ScheduleController.filter(filter)
	elif(request.method == 'GET' and day is not None):
		return ScheduleController.filter(day)


# Beacon route by id


@api.route('/schedules/<id>', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
@token_required
def schedule_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return ScheduleController.update(request, id)
    elif(request.method == 'GET'):
        return ScheduleController.show(id)
    elif(request.method == 'DELETE'):
        return ScheduleController.delete(id)

# Speakers endpoint


@api.route('/speakers', methods=['GET'])
@token_required
def speaker(*args, **kwargs):
    if(request.method == 'GET'):
        return SpeakerController.index()


@api.route('/speakers/<id>', methods=['PUT', 'PATCH', 'GET'])
@token_required
def speaker_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return SpeakerController.update(request, id)
    elif(request.method == 'GET'):
        return SpeakerController.show(id)

# Booth api


@api.route('/booths', methods=['PUT', 'PATCH', 'GET', 'POST'])
@token_required
def booth(*args, **kwargs):
    user = kwargs['user'].as_dict()
    if(request.method == 'PUT' or request.method == 'PATCH'):
        if(user['role_id'] == ROLE['booth']):
            return BoothController.update(request, user['id'])
        return 'Unauthorized'
    elif(request.method == 'POST'):
        return BoothController.create(request)
    elif(request.method == 'GET'):
        return BoothController.index(request)

# Booth route by id


@api.route('/booths/<booth_id>', methods=['GET', 'PUT', 'PATCH'])
@token_required
def booth_id(booth_id, *args, **kwargs):
    if(request.method == 'GET'):
        return BoothController.show(booth_id)
    return BoothController.update(request, None, booth_id)


# Point endpoint


@api.route('/points/transfer', methods=['POST'])
@token_required
def transfer_points(*args, **kwargs):
    user = kwargs['user'].as_dict()
    if(user['role_id'] == 1 or user['role_id'] == 3):
        return PointsController.transfer_point(request, user['id'])
    return 'You cannot transfer points'


@api.route('/points/logs', methods=['GET'])
@token_required
def transfer_points_log(*args, **kwargs):
    user = kwargs['user'].as_dict()
    return PointsController.transfer_point_log(request, user)

# User Photo api


@api.route('/user/photo', methods=['GET', 'POST', 'DELETE'])
@token_required
def user_photo(*args, **kwargs):
	user_id = kwargs['user'].id
	if(request.method == 'POST'):
		return UserPhotoController.create(request, user_id)
	elif(request.method == 'DELETE'):
		return UserPhotoController.delete(user_id)
	elif(request.method == 'GET'):
		return UserPhotoController.show(user_id)


@api.route('/user/photos', methods=['GET'])
@token_required
def user_photos(*args, **kwargs):
    if(request.method == 'GET'):
        return UserPhotoController.index()

# Ticket Transfer endpoint


@api.route('/tickets/transfer/logs', methods=['GET'])
@token_required
def ticket_transfer_logs(*args, **kwargs):
    user = kwargs['user'].as_dict()
    return TicketTransferController.ticket_transfer_logs(user)


@api.route('/tickets/transfer', methods=['POST'])
@token_required
def ticket_transfer(*args, **kwargs):
    user = kwargs['user'].as_dict()
    return TicketTransferController.ticket_transfer(request, user)

# Speaker Document api
# UPLOAD FILES AND GET LIST OF FILES UPLOADED BY THE SPEAKER


@api.route('/documents', methods=['POST', 'GET'])
@token_required
def speaker_document(*args, **kwargs):
    user = kwargs['user'].as_dict()
    if(request.method == 'POST'):
        return SpeakerDocumentController.create(request, user)
    elif(request.method == 'GET'):
        return SpeakerDocumentController.show(user)

@api.route('/document_speaker_admin', methods=['POST'])
@token_required
def speaker_document_admin(*args, **kwargs):
    user = kwargs['user'].as_dict()
    print(request);
    if(request.method == 'POST'):
        return SpeakerDocumentController.admin_create(request, user)

# GET SPECIFIC FILE UPLOADED BY THE SPEAKER || DELETE SPECIFIC FILE


@api.route('/documents/<id>', methods=['DELETE', 'GET'])
@token_required
def _speaker_document(id, *args, **kwargs):
    user = kwargs['user'].as_dict()
    if(request.method == 'GET'):
        return SpeakerDocumentController.view(id)
    elif(request.method == 'DELETE'):
        return SpeakerDocumentController.delete(user, id)

# GET LIST OF FILES BASED ON USER ID


@api.route('/speaker/<speaker_id>/documents', methods=['GET'])
@token_required
def speaker_document_user(speaker_id, *args, **kwargs):
    if(request.method == 'GET'):
        return SpeakerDocumentController._show(speaker_id)

# Newsletter api


@api.route('/newsletters', methods=['GET', 'POST'])
def newsletter(*args, **kwargs):
    if(request.method == 'POST'):
        return NewsletterController.create(request)
    elif(request.method == 'GET'):
        return NewsletterController.index()

# Newsletter route by id


@api.route('/newsletters/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def newsletter_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return NewsletterController.update(request, id)
    elif(request.method == 'GET'):
        return NewsletterController.show(id)
    elif(request.method == 'DELETE'):
        return NewsletterController.delete(id)

# User ticket api

# PATCH - ticket_id, receiver_id


@api.route('/user/tickets', methods=['GET', 'PATCH', 'PUT'])
@token_required
def user_tickets(*args, **kwargs):
    user_id = kwargs['user'].id
    if(request.method == 'GET'):
        return UserTicketController.show(user_id)
    elif(request.method == 'PATCH' or request.method == 'PUT'):
        return UserTicketController.update(user_id, request)


@api.route('/user/tickets/checkin', methods=['POST'])
@token_required
def check_in(*args, **kwargs):
    return UserTicketController.check_in(request)


# Attendee api


@api.route('/attendees', methods=['GET'])
@token_required
def attendees(*args, **kwargs):
    if(request.method == 'GET'):
        return AttendeeController.index(request)

# Attendee route by id


@api.route('/attendees/<id>', methods=['GET'])
@token_required
def attendees_id(id, *args, **kwargs):
    if(request.method == 'GET'):
        return AttendeeController.show(id)


# User list

@api.route('/users', methods=['GET'])
@token_required
def users(*args, **kwargs):
    if(request.method == 'GET'):
        return UserController.index(request)

# User detail/ route by id


@api.route('/users/<id>', methods=['GET'])
@token_required
def user_id(id, *args, **kwargs):
    if(request.method == 'GET'):
        return UserController.show(id)

# Add new User


@api.route('/users', methods=['POST'])
@token_required
def add_user(*args, **kwargs):
    if(request.method == 'POST'):
        return UserController.add(request)


# Edit User

@api.route('/users/<id>', methods=['PUT'])
@token_required
def edit_user(id, *args, **kwargs):
    if(request.method == 'PUT'):
        return UserController.update(request, id)

# Delete User


@api.route('/users/<id>', methods=['DELETE'])
@token_required
def delete_user(id, *args, **kwargs):
    if(request.method == 'DELETE'):
        return UserController.delete(id)

# Payment api


@api.route('/payments', methods=['POST', 'GET'])
@token_required
def payment(*args, **kwargs):
    filter = request.args.get('transaction_status')
    user = kwargs['user'].as_dict()
    if (request.method == 'POST'):
        return PaymentController.create(request)
    elif(request.method == 'GET'):
        if(user['role_id'] == ROLE['admin'] and filter):
            return PaymentController.admin_filter_payments(filter)
        elif (user['role_id'] == ROLE['admin'] and filter is None):
            return PaymentController.admin_get_payments()
        else:
            return PaymentController.get_payments(user['id'])


@api.route('/payments/authorize', methods=['POST'])
@token_required
def authorize_credit_card(*args, **kwargs):
	return PaymentController.authorize(request)


@api.route('/payments/status/<id>', methods=['PATCH', 'PUT'])
@token_required
def status(id, *args, **kwargs):
    if (request.method == 'PATCH' or request.method == 'PUT'):
        return PaymentController.status(id)


@api.route('/payments/<payment_id>', methods=['GET'])
@token_required
def show_payment(payment_id, *args, **kwargs):
    user = kwargs['user'].as_dict()
    if(user['role_id'] == ROLE['admin']):
        return PaymentController.admin_show_payment(payment_id)
    else:
        return PaymentController.show_payment(payment_id)

# Referal api


@api.route('/referals', methods=['GET', 'POST'])
@token_required
def referal(*args, **kwargs):
    if(request.method == 'POST'):
        return ReferalController.create(request)
    elif(request.method == 'GET'):
        return ReferalController.index()

# Referal route by id


@api.route('/referals/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def referal_id(id, *args, **kwargs):
    if(request.method == 'PUT' or request.method == 'PATCH'):
        return ReferalController.update(request, id)
    elif(request.method == 'DELETE'):
        return ReferalController.delete(id)
    elif(request.method == 'GET'):
        return ReferalController.show(id)


# get referal id

@api.route('/referals/check', methods=['POST'])
@token_required
def check_referal(*args, **kwargs):
    return ReferalController.check(request)


@api.route('/me', methods=['GET'])
@token_required
def me(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserController.show(user['id'])


@api.route('/partners/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def partners_id(id, *args, **kwargs):
    if(request.method == 'GET'):
        return PartnerController.show(id)
    elif(request.method == 'PATCH' or request.method == 'PUT'):
        return PartnerController.update(id, request)
    else:
        return PartnerController.delete(id)


@api.route('/partners', methods=['GET', 'POST'])
@token_required
def partners(*args, **kwargs):
    if(request.method == 'GET'):
        return PartnerController.index(request)
    else:
        return PartnerController.create(request)


@api.route('/entrycashlogs', methods=['GET', 'POST'])
@token_required
def get_entry_cash_log(*args, **kwargs):
    if(request.method == 'POST'):
        return EntryCashLogController.create(request)
    elif(request.method == 'GET'):
        return EntryCashLogController.index(request)


@api.route('/entrycashlogs/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@token_required
def entry_cash_log_id(id, *args, **kwargs):
    if (request.method == 'PUT' or request.method == 'PATCH'):
        return EntryCashLogController.update(request, id)
    elif (request.method == 'DELETE'):
        return EntryCashLogController.delete(id)
    elif (request.method == 'GET'):
        return EntryCashLogController.show(id)


@api.route('/sponsors', methods=['GET', 'POST'])
@token_required
def get_sponsors(*args, **kwargs):
    if(request.method == 'GET'):
        return SponsorController.index(request)
    elif(request.method == 'POST'):
        return SponsorController.create(request)


@api.route('/sponsors/<id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
@token_required
def get_sponsor_id(id, *args, **kwargs):
    if (request.method == 'GET'):
        return SponsorController.show(id)
    elif (request.method in ['PATCH', 'PUT']):
        return SponsorController.update(id, request)
    else:
        return SponsorController.delete(id)


@api.route('/sponsors/<id>/logs', methods=['GET', 'POST'])
@token_required
def get_sponsor_log(id, *args, **kwargs):
    if (request.method == 'GET'):
        return SponsorController.get_logs(id)
    elif (request.method in 'POST'):
        return SponsorController.create_log(request, id)


# Add rundown list API
@api.route('/rundownlist', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
@token_required
def rundown(*args, **kwargs):
    if (request.method == 'GET'):
        return RundownListController.index(request)
    elif (request.method == 'POST'):
        return RundownListController.create(request)
    elif (request.method in ['PATCH', 'PUT']):
        return RundownListController.update(request)   
    else:
        return RundownListController.delete()