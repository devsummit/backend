import os
import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order import Order
from app.models.order_details import OrderDetails
from app.models.user import User
from app.models.payment import Payment
from app.models.order_verification import OrderVerification
from app.models.base_model import BaseModel
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from app.services.user_ticket_service import UserTicketService
from flask import current_app
from PIL import Image
from app.configs.constants import IMAGE_QUALITY
from app.services.helper import Helper 
from werkzeug import secure_filename


class OrderVerificationService(BaseService):
	
	def get(self):
		orderverifications = BaseModel.as_list(db.session.query(OrderVerification).filter_by(is_used=0).all())
		for entry in orderverifications:
			if entry['payment_proof']:
				entry['payment_proof'] = Helper().url_helper(entry['payment_proof'], current_app.config['GET_DEST'])
			else:
				entry['payment_proof'] = ""
		return orderverifications

	def create(self, payload):
		response = ResponseBuilder()
		orderverification_query = db.session.query(OrderVerification).filter_by(order_id=payload['order_id'])
		orderverification = orderverification_query.first()
		payment_proof = self.save_file(payload['payment_proof']) if payload['payment_proof'] is not None else None
		if orderverification:
			if orderverification.payment_proof is not None:
				Helper().silent_remove(current_app.config['STATIC_DEST'] + orderverification.payment_proof)
			orderverification_query.update({
				'payment_proof': payment_proof,
				'updated_at': datetime.datetime.now()
			})
		else:
			orderverification = OrderVerification()
			orderverification.user_id = payload['user_id']
			orderverification.order_id = payload['order_id']
			orderverification.payment_proof = payment_proof
			db.session.add(orderverification)
		try:
			db.session.commit()
			result = orderverification.as_dict()
			result['payment_proof'] = Helper().url_helper(result['payment_proof'], current_app.config['GET_DEST'])
			return response.set_data(result).set_message('Data created succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def show(self, id):
		response = ResponseBuilder()
		orderverification = db.session.query(OrderVerification).filter_by(order_id=id).first()
		data = orderverification.as_dict() if orderverification else None
		if data:
			if data['payment_proof']:
				data['payment_proof'] = Helper().url_helper(data['payment_proof'], current_app.config['GET_DEST'])
			else:
				data['payment_proof'] = ""
			return response.set_data(data).build()
		return response.set_error(True).set_message('data not found').set_data(None).build()


	def update(self, id, payload):
		response = ResponseBuilder()
		orderverification = db.session.query(OrderVerification).filter_by(id=id)
		data = orderverification.first().as_dict() if orderverification.first() else None
		if data['payment_proof'] is not None and payload['payment_proof']:
			Helper().silent_remove(current_app.config['STATIC_DEST'] + data['payment_proof'])
		if data is None:
			return response.set_error(True).set_message('data not found').set_data(None).build()
		payment_proof = self.save_file(payload['payment_proof']) if payload['payment_proof'] is not None else None
		try:
			orderverification = db.session.query(OrderVerification).filter_by(id=id)			
			orderverification.update({
				'user_id': payload['user_id'],
				'order_id': payload['order_id'],
				'payment_proof': payment_proof,
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = orderverification.first()
			return response.set_data(data.as_dict()).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).build()

	def delete(self, id):
		response = ResponseBuilder()
		orderverification = db.session.query(OrderVerification).filter_by(id=id).first()
		if orderverification.payment_proof is not None:
			Helper().silent_remove(current_app.config['STATIC_DEST'] + orderverification.payment_proof)
		orderverification = db.session.query(OrderVerification).filter_by(id=id)
		if orderverification.first() is not None:
			orderverification.delete()
			db.session.commit()
			return response.set_message('Order Verification entry was deleted').build()
		else:
			data = 'Entry not found'
			return response.set_data(None).set_message(data).set_error(True).build()

	def save_file(self, file, id=None):
		image = Image.open(file, 'r')
		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
			if (Helper().allowed_file(file.filename, ['jpg', 'jpeg', 'png'])):
				image = image.convert("RGB")
			filename = secure_filename(file.filename)
			filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
			image.save(os.path.join(current_app.config['POST_PAYMENT_PROOF_DEST'], filename), quality=IMAGE_QUALITY, optimize=True)
			return current_app.config['SAVE_PAYMENT_PROOF_DEST'] + filename
		else:
			return None

	def verify(self, id):
		response = ResponseBuilder()
		orderverification_query = db.session.query(OrderVerification).filter_by(id=id)
		orderverification = orderverification_query.first()
		if orderverification.is_used is not 1:
			user = db.session.query(User).filter_by(id=orderverification.user_id).first()
			items = db.session.query(OrderDetails).filter_by(order_id=orderverification.order_id).all()
			for item in items:
				for i in range(0, item.count):
					payload = {}
					payload['user_id'] = user.id
					payload['ticket_id'] = item.ticket_id
					UserTicketService().create(payload)
			orderverification_query.update({
				'is_used': 1
			})
			payment_query = db.session.query(Payment).filter_by(order_id=orderverification.order_id)
			payment_query.update({
				'transaction_status': 'capture'
			})
			db.session.commit()
			return response.set_data(None).set_message('ticket created').build()
		else:
			return response.set_data(None).set_message('This payment has already verified').build()
