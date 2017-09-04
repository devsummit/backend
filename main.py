from app.configs import settings
from app import create_app


if __name__ == "__main__":
	app = create_app(settings)
	app.run(host='0.0.0.0')
