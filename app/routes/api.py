'''
put api route in here
'''
from flask import Blueprint

# import middlewares
from app.middlewares.authentication import token_required

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
@token_required
def index(*args, **kwargs):
	return 'api index'