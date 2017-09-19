# settings.py
import os
from dotenv import load_dotenv

load_dotenv('.env')

# app setting only for development purpose comment this out if not used
DEBUG = True

# constants
API_BASE_URL = os.environ.get("API_BASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

# sqlite database file path
SQLALCHEMY_DATABASE_URI = 'mysql://' + os.environ.get("DB_USERNAME") + ':' + os.environ.get("DB_PASSWORD") \
							+ '@' + os.environ.get("DB_HOST") + '/' + os.environ.get("DB_NAME")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# default saving, database saving & domain based url

POST_STAGE_PHOTO_DEST = 'app/static/images/stages/'
SAVE_STAGE_PHOTO_DEST = 'images/stages/'
POST_PARTNER_PHOTO_DEST = 'app/static/images/partners/'
SAVE_PARTNER_PHOTO_DEST = 'images/partners/'
POST_USER_PHOTO_DEST = 'app/static/images/users/'
SAVE_USER_PHOTO_DEST = 'images/users/'
POST_BOOTH_PHOTO_DEST = 'app/static/images/booths/'
SAVE_BOOTH_PHOTO_DEST = 'images/booths/'
GET_DEST = 'static/'
STATIC_DEST = 'app/static/'

# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
