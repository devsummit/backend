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
                            + '@' + os.environ.get("DB_HOST") + '/' + os.environ.get("DB_NAME") + '?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# email server
MAIL_SERVER = 'email-smtp.us-west-2.amazonaws.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'AKIAIWLWWJ3TNRVLQO4Q'
MAIL_DEFAULT_SENDER = 'noreply@devsummit.io'
MAIL_PASSWORD = 'AuWb80Fvq2GDMeYwyZBkaiIcAML8Tu2e9Pcq+1YBDbk4'
MAIL_SUPPRESS_SEND = False
# administrator list
ADMINS = ['noreply@devsummit.io']
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
# payment proof
POST_PAYMENT_PROOF_DEST = 'app/static/images/payment_proof/'
SAVE_PAYMENT_PROOF_DEST = 'images/payment_proof/'
#PROPOSAL DOC
POST_PROPOSAL_DOC_DEST = 'app/static/documents/proposals/'
SAVE_PROPOSAL_DOC_DEST = 'documents/proposals/'
GET_PROPOSAL_DOC_DEST = 'static/'
STATIC_DEST = 'app/static/'
# These are the extentions that we are accepting to be upload
ALLOWED_PROPOSAL_DOC_EXTENSIONS = set(['pdf', 'ppt'])
#LOGO HACKER TEAM
POST_HACKER_TEAM_PIC_DEST = 'app/static/images/hackerteam_logo/'
SAVE_HACKER_TEAM_PIC_DEST = 'images/hackerteam_logo/'

GET_DEST = 'static/'
STATIC_DEST = 'app/static/'

# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#This is the registered url route for email service
EMAIL_HANDLER_ROUTE = 'email-verification'

#This is to set local timezone to GMT+7 for admin
LOCAL_TIME_ZONE = 7
