from flask import current_app


import datetime
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# import classes
from app.models.base_model import BaseModel
from app.models import db


class User(db.Model, BaseModel):

	__tablename__ = 'users'
	# displayed fields
	visible = ['id', 'first_name', 'last_name', 'username', 'email', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	username = db.Column(db.String, index=True, unique=True)
	email = db.Column(db.String, index=True, unique=True)
	password = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()

	def hash_password(self, password):
		self.password = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password, password)

	def generate_auth_token(self, expiration=6000):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user = db.session.query(User).filter_by(id=data['id']).first()
		return user

	def generate_refresh_token(self):
		return secrets.token_hex(8)
