import datetime

# import classes
from app.models.base_model import BaseModel
from app.models import db

class User(db.Model, BaseModel):
	# table name
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