from app.configs import settings
from app import create_app
from app.models import socketio


if __name__ == "__main__":
	app = create_app(settings)
	socketio.init_app(app)
	socketio.run(app, host='0.0.0.0', port=8081)
