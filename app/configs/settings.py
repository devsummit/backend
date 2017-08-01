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
