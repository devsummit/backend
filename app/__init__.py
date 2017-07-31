from flask import Flask

# routes
from app.routes.main import main
from app.routes.api import api

def create_app(configuration):
	app = Flask(__name__)

	# set configuration
	app.config.from_object(configuration)

	# register blueprints
	app.register_blueprint(main)
	app.register_blueprint(api, url_prefix=app.config['API_BASE_URL'])

	return app
