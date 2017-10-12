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


# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'andy.developmode@gmail.com'
MAIL_DEFAULT_SENDER = 'admin@devsummit.com'
MAIL_PASSWORD = 'lmwdurszelzyxthl'
MAIL_SUPPRESS_SEND = False
# administrator list
ADMINS = ['andy.developmode@gmail.com']

# default saving, database saving & domain based url
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
POST_STAGE_PHOTO_DEST = 'app/static/images/stages/'
SAVE_STAGE_PHOTO_DEST = 'images/stages/'
POST_PARTNER_PHOTO_DEST = 'app/static/images/partners/'
SAVE_PARTNER_PHOTO_DEST = 'images/partners/'
POST_USER_PHOTO_DEST = 'app/static/images/users/'
SAVE_USER_PHOTO_DEST = 'images/users/'
POST_FEED_PHOTO_DEST = 'app/static/images/feeds/'
SAVE_FEED_PHOTO_DEST = 'images/feeds/'
POST_BOOTH_PHOTO_DEST = 'app/static/images/booths/'
SAVE_BOOTH_PHOTO_DEST = 'images/booths/'
# prize lists
POST_PRIZE_LIST_DEST = 'app/static/images/prize_lists/'
SAVE_PRIZE_LIST_DEST = 'images/prize_lists/'
# booth gallery
POST_BOOTH_GALL_DEST = 'app/static/images/booths/galleries/'
SAVE_BOOTH_GALL_DEST = 'images/booths/galleries/'
# sponsor picture
POST_SPONSOR_PIC_DEST = 'app/static/images/sponsor/'
SAVE_SPONSOR_PIC_DEST = 'images/sponsor/'

GET_DEST = 'static/'
STATIC_DEST = 'app/static/'

# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
