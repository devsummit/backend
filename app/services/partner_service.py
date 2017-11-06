import os
import datetime
from flask import current_app
from app.models import db
from app.services.helper import Helper
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import secure_filename
from app.models.partners import Partner
from app.models.partner_pj import PartnerPj
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class PartnerService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage
		self.temp_image = 'images/partners/empty-profile-grey.jpg'

	def get(self, request):
		self.total_items = Partner.query.count()
		if request.args.get('page'):
			self.page = request.args.get('page')
		else:
			self.perpage = self.total_items
			self.page = 1
		self.base_url = request.base_url
        # paginate
		paginate = super().paginate(db.session.query(Partner))
		paginate = super().transform()
		for item in paginate['data']:
			if item['photo']:
				item['photo']= Helper().url_helper(item['photo'], current_app.config['GET_DEST'])
				continue
			else:
				item['photo']=Helper().url_helper(self.temp_image, current_app.config['GET_DEST'])
				continue
		response = ResponseBuilder()
		return response.set_data(paginate['data']).set_links(paginate['links']).build()

	def show(self, id):
		response = ResponseBuilder()
		partner = db.session.query(Partner).filter_by(id=id).first()
		data = {}
		data = partner.as_dict() if partner else None
		return response.set_data(data).build()

	def create(self, payloads):
		response = ResponseBuilder()
		partner = Partner()
		photo = self.save_file(payloads['photo'])
		partner.name = payloads['name']
		partner.email = payloads['email']
		partner.website = payloads['website']
		partner.photo = photo
		partner.type = payloads['type']

		db.session.add(partner)
		try:
			db.session.commit()
			data = partner.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def save_file(self, file, id=None):
		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
				filename = secure_filename(file.filename)
				filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
				file.save(os.path.join(current_app.config['POST_PARTNER_PHOTO_DEST'], filename))
				if id:
					temp_partner = db.session.query(Partner).filter_by(id=id).first()
					partner_photo = temp_partner.as_dict() if temp_partner else None
					if partner_photo is not None and partner_photo['photo'] is not None:
						Helper().silent_remove(current_app.config['STATIC_DEST'] + partner_photo['photo'])
				return current_app.config['SAVE_PARTNER_PHOTO_DEST'] + filename
		else:
			return None

	def update(self, payloads, id):
		response = ResponseBuilder()
		try:
			partner = db.session.query(Partner).filter_by(id=id)
			file = payloads['photo']
			photo = None
			photo = self.save_file(file, id)
			partner.update({
				'name': payloads['name'],
				'email': payloads['email'],
				'website': payloads['website'],
				'type': payloads['type'],
				'updated_at': datetime.datetime.now()
			})
			if photo:
				partner.update({
					'photo': photo,
					'updated_at': datetime.datetime.now()
				})
			db.session.commit()
			data = partner.first().as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).build()

	def delete(self, id):
		response = ResponseBuilder()
		partner = db.session.query(Partner).filter_by(id=id)
		if partner.first() is not None:
			# delete row
			partner.delete()
			db.session.commit()
			return response.set_message('data deleted').build()
		else:
			data = 'data not found'
			return response.set_data(None).set_message(data).set_error(True).build()

	def filter(self, filter, request):
		response = ResponseBuilder()
		partners = db.session.query(Partner).filter_by(type=filter).all()
		results = []
		for partner in partners:
			pj = db.session.query(PartnerPj).filter_by(partner_id=partner.id).first()
			data = partner.as_dict()
			data['user_id'] = pj.user_id if pj else None
			results.append(data)
		result = response.set_data(results).build()
		return result
