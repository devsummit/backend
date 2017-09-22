from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()