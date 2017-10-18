import os
import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from app.services.base_service import BaseService

#import model class
from app.models.logs import Logs
from app.models.base_model import BaseModel
from app.builders.response_builder import ResponseBuilder


class LogsService(BaseService):

	def create_log(self, description):
		response = ResponseBuilder()
		self.log = Logs()
		self.log.description = description
		db.session.add(self.log)
		try:
			db.session.commit()
			return response.set_message('Log has been create').set_data(None).build()
		except SQLAlchemyError as e:
			return response.set_message('Cant create log').set_data(e.orig.args).build()
