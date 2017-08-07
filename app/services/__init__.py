# services import
from app.services.user_service import UserService
from app.services.ticket_service import TicketService

# models import
from app.models.user import User
from app.models.ticket import Ticket
from app.models.access_token import AccessToken

# Intantiate models
user = User()
ticket = Ticket()
access_token = AccessToken()

# instantiate service
userservice = UserService(user, access_token)
ticketservice = TicketService(ticket)
