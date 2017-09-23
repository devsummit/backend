import os
import datetime
from flask import current_app
from app.models import db
from app.services.helper import Helper 
from werkzeug import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from app.models.feed import Feed
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class FeedService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage

	def get(self, request, page):
		self.total_items = Feed.query.count()
		print(self.total_items, 'total')
		print(page)
		if page is not None:
			self.page = request.args.get('page')
		else:
			self.perpage = self.total_items
			self.page = 1
		self.base_url = request.base_url
        # paginate
		paginate = super().paginate(db.session.query(Feed).order_by(Feed.created_at.desc()))
		paginate = super().include_user()
		response = ResponseBuilder()
		for row in paginate['data']:
			if row['attachment'] is not None:
				row['attachment'] = Helper().url_helper(row['attachment'], current_app.config['GET_DEST'])
		return response.set_data(paginate['data']).set_links(paginate['links']).build()

	def show(self, id):
		response = ResponseBuilder()
		feed = db.session.query(Feed).filter_by(id=id).first()
		data = {}
		data = feed.as_dict() if feed else None
		data['user'] = feed.user.include_photos().as_dict()
		data['attachment'] = Helper().url_helper(data['attachment'], current_app.config['GET_DEST']) if data['attachment'] is not None else None
		return response.set_data(data).build()

	def create(self, payloads):
		response = ResponseBuilder()
		feed = Feed()
		attachment = self.save_file(payloads['attachment']) if payloads['attachment'] is not None else None
		feed.message = payloads['message']
		feed.attachment = attachment
		feed.user_id = payloads['user_id']
		db.session.add(feed)
		try:
			db.session.commit()
			user = feed.user.include_photos().as_dict()
			del user['fcmtoken']
			data = feed.as_dict()
			data['attachment'] = Helper().url_helper(data['attachment'], current_app.config['GET_DEST']) if data['attachment'] is not None else None
			data['user'] = user
			# data['user'] = feed.user.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def save_file(self, file, id=None):
		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
				filename = secure_filename(file.filename)
				filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
				file.save(os.path.join(current_app.config['POST_FEED_PHOTO_DEST'], filename))
				return current_app.config['SAVE_FEED_PHOTO_DEST'] + filename
		else:
			return None
