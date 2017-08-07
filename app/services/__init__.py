# services import
from app.services.user_service import UserService
from app.services.ticket_service import TicketService
from app.services.stage_service import StageService

# models import
from app.models.user import User
from app.models.ticket import Ticket
from app.models.stage import Stage
from app.models.access_token import AccessToken

# Intantiate models
user = User()
ticket = Ticket()
stage = Stage()
access_token = AccessToken()

# instantiate service
userservice = UserService(user, access_token)
ticketservice = TicketService(ticket)
stageservice = StageService(stage)
