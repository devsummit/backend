# services import
from app.services.user_service import UserService
from app.services.ticket_service import TicketService
from app.services.stage_service import StageService
from app.services.beacon_service import BeaconService
from app.services.spot_service import SpotService
from app.services.order_service import OrderService
from app.services.order_details_service import OrderDetailsService
from app.services.event_service import EventService
from app.services.schedule_service import ScheduleService
from app.services.points_transaction_service import PointsTransactionService
from app.services.user_photo_service import UserPhotoService
from app.services.speaker_service import SpeakerService
from app.services.ticket_transfer_service import TicketTransferService
from app.services.speaker_document_service import SpeakerDocumentService
from app.services.newsletter_service import NewsletterService
from app.services.booth_service import BoothService
from app.services.user_ticket_service import UserTicketService
from app.services.attendee_service import AttendeeService
from app.services.payment_service import PaymentService 
from app.services.referal_service import ReferalService 
from app.services.base_service import BaseService

# instantiate service
userservice = UserService(10)  # number of item per page
ticketservice = TicketService()
stageservice = StageService()
beaconservice = BeaconService()
spotservice = SpotService()
orderservice = OrderService()
orderdetailservice = OrderDetailsService()
eventservice = EventService(10)  # number of item per page
scheduleservice = ScheduleService()
pointtransactionservice = PointsTransactionService()
userphotoservice = UserPhotoService()
speakerservice = SpeakerService()
tickettransferservice = TicketTransferService()
speakerdocumentservice = SpeakerDocumentService()
newsletterservice = NewsletterService()
boothservice = BoothService(10)  # number of item per page
userticketservice = UserTicketService()
attendeeservice = AttendeeService(10)  # number of item per page
paymentservice = PaymentService()
referalservice = ReferalService()
baseservice = BaseService()
