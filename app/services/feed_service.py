import os
import datetime
from PIL import Image
from flask import current_app
from app.models import db
from app.configs.constants import ROLE, IMAGE_QUALITY
from app.services.helper import Helper 
from werkzeug import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from app.models.feed import Feed
from app.models.comments import Comment
from app.models.sponsor import Sponsor
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class FeedService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage

	def get(self, request, page):
		self.total_items = Feed.query.count()
		if page is not None:
			self.page = request.args.get('page')
		else:
			self.perpage = 10
			self.page = 1
		self.base_url = request.base_url
        # paginate
		paginate = super().paginate(db.session.query(Feed).order_by(Feed.created_at.desc()))
		paginate = super().include_sponsor()
		response = ResponseBuilder()
		for row in paginate['data']:
			if row['attachment'] is not None:
				row['attachment'] = Helper().url_helper(row['attachment'], current_app.config['GET_DEST'])
			row['comment_count'] = Comment.query.filter_by(feed_id=row['id']).count()
		return response.set_data(paginate['data']).set_links(paginate['links']).build()

	def show(self, id):
		response = ResponseBuilder()
		feed = db.session.query(Feed).filter_by(id=id).first()
		if feed is None:
			return response.set_data(None).set_error(True).set_message('feed not found').build()
		data = {}
		data = feed.as_dict() if feed else None
		data['user'] = feed.user.include_photos().as_dict()
		data['attachment'] = Helper().url_helper(data['attachment'], current_app.config['GET_DEST']) if data['attachment'] is not None else None
		data['comment_count'] = Comment.query.filter_by(feed_id=data['id']).count()

		return response.set_data(data).build()

	def delete(self, user, id):
		response = ResponseBuilder()
		feed = db.session.query(Feed).filter_by(id=id)
		if feed.first() is None:
			return response.set_error(True).set_data(None).set_message('feed not found').build()

		if user['role_id'] != ROLE['admin']:
			if feed.first().as_dict()['user_id'] != user['id']:
				print(feed.first().as_dict())
				return response.set_error(True).set_data(None).set_message('you are unauthorized to delete this feed').build()
		feed.delete()
		try:
			db.session.commit()
			return response.set_data(None).set_message('Feed deleted').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def create(self, payloads):
		response = ResponseBuilder()
		feed = Feed()
		sponsor = db.session.query(Sponsor).filter_by(id=payloads['sponsor_id']).first()
		attachment = self.save_file(payloads['attachment']) if payloads['attachment'] is not None else None
		feed.message = payloads['message']
		feed.attachment = attachment
		feed.user_id = payloads['user_id']
		feed.type = payloads['type']
		feed.redirect_url = payloads['redirect_url']
		feed.sponsor_id = payloads['sponsor_id']
		db.session.add(feed)
		try:
			db.session.commit()
			user = feed.user.include_photos().as_dict()
			del user['fcmtoken']
			data = feed.as_dict()
			data['attachment'] = Helper().url_helper(data['attachment'], current_app.config['GET_DEST']) if data['attachment'] is not None else None
			if 'user' in payloads['type']:
				data['user'] = user
			elif 'sponsor' in payloads['type']:
				data['user'] = sponsor.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()
	
	#this method use for create sponsor feeds in admin panel
	#because i can't move file from sponsor_template
	#the different this method with method create just in attachment type
	def sponsor_create(self, payloads):
		response = ResponseBuilder()
		feed = Feed()
		for key in payloads:
			setattr(feed, key, payloads[key])
		db.session.add(feed)
		try:
			db.session.commit()
			user = feed.user.include_photos().as_dict()
			sponsor = db.session.query(Sponsor).filter_by(id=payloads['sponsor_id']).first()		
			del user['fcmtoken']
			data = feed.as_dict()
			data['attachment'] = Helper().url_helper(data['attachment'], current_app.config['GET_DEST']) if data['attachment'] is not None else None
			if 'user' in payloads['type']:
				data['user'] = user
			elif 'sponsor' in payloads['type']:
				data['user'] = sponsor.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def save_file(self, file, id=None):
		image = Image.open(file, 'r')

		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
			if (Helper().allowed_file(file.filename, ['jpg', 'jpeg'])):
				image = image.convert("RGB")
			filename = secure_filename(file.filename)
			filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
			image.save(os.path.join(current_app.config['POST_FEED_PHOTO_DEST'], filename), quality=IMAGE_QUALITY, optimize=True)
			return current_app.config['SAVE_FEED_PHOTO_DEST'] + filename
		else:
			return None

	def bannedfeeds(self, feed_id):
		response = ResponseBuilder()
		self.model_feed = db.session.query(Feed).filter_by(id=feed_id)
		if self.model_feed.first() is None:
			return response.set_error(True).set_message('feed not found').build()
		if self.model_feed.first().deleted_at is not None:
			return response.set_error(True).set_message('feed already banned').build()
		self.model_feed.update({
			'deleted_at':datetime.datetime.now()
		})
		try:
			db.session.commit()
			return response.set_data(None).set_message('Success').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()