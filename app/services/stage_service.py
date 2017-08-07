import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.stage import Stage


class StageService():

	def __init__(self, model_stage):
		self.model_stage = model_stage

	def get(self):
		stages = db.session.query(Stage).all()
		return stages

	def show(self, id):
		stage = db.session.query(Stage).filter_by(id=id).first()
		return stage

	def create(self, payloads):
		self.model_stage.name = payloads['name']
		self.model_stage.stage_type = payloads['stage_type']
		self.model_stage.information = payloads['information']
		db.session.add(self.model_stage)
		try:
			db.session.commit()
			data = self.model_stage.as_dict()
			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def update(self, payloads, id):
		try:
			self.model_stage = db.session.query(Stage).filter_by(id=id)
			self.model_stage.update({
				'name': payloads['name'],
				'stage_type': payloads['stage_type'],
				'information': payloads['information'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_stage.first().as_dict()
			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def delete(self, id):
		self.model_stage = db.session.query(Stage).filter_by(id=id)
		if self.model_stage.first() is not None:
			# delete row
			self.model_stage.delete()
			db.session.commit()
			return {
				'error': False,
				'data': None
			}
		else:
			data = 'data not found'
			return {
				'error': True,
				'data': data
			}
