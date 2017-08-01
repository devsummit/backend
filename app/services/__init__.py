from app.services.user_service import UserService
from app.models.user import User
from app.models.access_token import AccessToken


user = User()
access_token = AccessToken()

userservice = UserService(user, access_token)
