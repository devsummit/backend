from flask import Flask

# routes
from app.routes.main import main
from app.routes.api import api
from app.routes.auth import auth

# import some global configs
from app.configs.constants import ROLE

# db instance
from app.models import db


def create_app(configuration):
	app = Flask(__name__)

	# set configuration
	app.config.from_object(configuration)

	# database
	db.init_app(app)

	# register blueprints
	app.register_blueprint(main)
	app.register_blueprint(api, url_prefix=app.config['API_BASE_URL'])
	app.register_blueprint(auth, url_prefix='/auth')

	# define global object here to used across all templates
	app.jinja_env.globals.update(roles=ROLE)

	return app
