from flask import Flask

# routes
from app.routes.main import main
from app.routes.auth import auth
from app.routes.api.v1 import events


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
	app.register_blueprint(auth, url_prefix='/auth')
	app.register_blueprint(events, url_prefix=app.config['API_BASE_URL'])
	
	return app
