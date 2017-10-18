import datetime
from app.models import db
from app.models.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from flask import request, current_app
from app.services.helper import Helper 
from werkzeug import secure_filename
import os
# import model class
from app.models.stage import Stage
from app.models.stage_photos import StagePhotos


class StageService():

	def get(self):
		stages = db.session.query(Stage).all()
		return stages

	def getPictures(self, stage_id):
		stage_pictures = BaseModel.as_list(db.session.query(StagePhotos).filter_by(stage_id=stage_id).all())
		for stage_picture in stage_pictures:
			stage_picture['url'] = Helper().url_helper(stage_picture['url'], current_app.config['GET_DEST'])
		return stage_pictures

	def show(self, id):
		stage = db.session.query(Stage).filter_by(id=id).first()
		return stage

	def showPicture(self, stage_id, id):
		stage_picture = db.session.query(StagePhotos).filter_by(stage_id=stage_id).filter_by(id=id).first()
		if(stage_picture is None):
			data = {
				'picture_exist': False
			}
			return {
				'data': data,
				'error': True,
				'message': 'Stage picture is not found'
			}
		stage_picture = stage_picture.as_dict()
		stage_picture['url'] = Helper().url_helper(stage_picture['url'], current_app.config['GET_DEST'])
		return {
			'data': stage_picture,
			'error': False,
			'message': 'Stage picture retrieved successfully'
		}

	def create(self, payloads):
		self.model_stage = Stage()
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

	def createPicture(self, payloads):
		file = request.files['image_file']
		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
			filename = secure_filename(file.filename)
			filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
			file.save(os.path.join(current_app.config['POST_STAGE_PHOTO_DEST'], filename))
			self.model_stage_picture = StagePhotos()
			self.model_stage_picture.stage_id = payloads['stage_id']
			self.model_stage_picture.url = current_app.config['SAVE_STAGE_PHOTO_DEST'] + filename
			db.session.add(self.model_stage_picture)
			try:
				db.session.commit()
				data = self.model_stage_picture.as_dict()
				data['url'] = Helper().url_helper(data['url'], current_app.config['GET_DEST'])
				return {
					'error': False,
					'data': data,
					'message': 'stage picture succesfully created'
				}
			except SQLAlchemyError as e:
				data = e.orig.args
				return {
					'error': True,
					'data': None,
					'message': data
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

	def updatePicture(self, payloads, stage_id, id):
		try:
			self.model_stage_picture = db.session.query(StagePhotos).filter_by(stage_id=stage_id).filter_by(id=id)
			exist = self.model_stage_picture.first()
			if(exist is None):
				data = {
					'picture_exist': False
				}
				return {
					'data': data,
					'error': True,
					'message': 'Stage picture is not found'
				}
			self.url = self.model_stage_picture.first().url
			os.remove(current_app.config['STATIC_DEST'] + self.url)
			file = request.files['image_file']
			if file and Helper.allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
				filename = secure_filename(file.filename)
				filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
				file.save(os.path.join(current_app.config['POST_STAGE_PHOTO_DEST'], filename))
				self.model_stage_picture.update({
					'url': current_app.config['SAVE_STAGE_PHOTO_DEST'] + filename,
					'updated_at': datetime.datetime.now()
				})
				db.session.commit()
				data = self.model_stage_picture.first().as_dict()
				data['url'] = Helper.url_helper(data['url'], current_app.config['GET_DEST'])
				return {
					'error': False,
					'data': data,
					'message': 'stage picture succesfully updated'
				}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': None,
				'message': data
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

	def deletePicture(self, stage_id, id):
		self.model_stage_picture = db.session.query(StagePhotos).filter_by(stage_id=stage_id).filter_by(id=id)
		if self.model_stage_picture.first() is not None:
			# delete row
			self.url = self.model_stage_picture.first().url
			os.remove(current_app.config['STATIC_DEST'] + self.url)
			self.model_stage_picture.delete()
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
