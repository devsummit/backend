import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.comments import Comment
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class CommentService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage

	def get_by_post_id(self, request, feed_id, page):
		self.total_items = Comment.query.filter_by(feed_id=feed_id).count()
		self.page = page
		self.base_url = request.base_url
		paginate = super().paginate(db.session.query(Comment).filter_by(feed_id=feed_id).order_by(Comment.created_at.desc()))
		paginate = super().include_user()
		response = ResponseBuilder()
		return response.set_data(paginate['data']).set_links(paginate['links']).build()


	def create(self, payloads):
		response = ResponseBuilder()
		comment = Comment()
		comment.content = payloads['content']
		comment.feed_id = payloads['feed_id']
		comment.user_id = payloads['user_id']
		db.session.add(comment)
		try:
			db.session.commit()
			user = comment.user.include_photos().as_dict()
			del user['fcmtoken']
			data = comment.as_dict()
			data['user'] = user
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()
