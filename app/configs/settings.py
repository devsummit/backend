import os
basedir = os.path.dirname(__file__)

# app setting only for development purpose comment this out if not used
DEBUG = True

# constants
API_BASE_URL = '/api/v1'
SECRET_KEY = 'supersecret'

# sqlite database file path
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../../app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# default saving, database saving & domain based url

POST_STAGE_PHOTO_DEST = 'app/static/images/stages/'
SAVE_STAGE_PHOTO_DEST = 'images/stages/'
POST_USER_PHOTO_DEST = 'app/static/images/users/'
SAVE_USER_PHOTO_DEST = 'images/users/'
GET_DEST = 'static/'
STATIC_DEST = 'app/static/'

# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
