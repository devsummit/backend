import datetime
from app.models import db
from app.models.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, request
from werkzeug import secure_filename
import os
# import model class
from app.models.stage import Stage
from app.models.stage_photos import StagePhotos

app = Flask(__name__)
# defaul saving directory
app.config['POST_STAGE_PHOTO_DEST'] = 'app/static/images/stages/'
app.config['SAVE_STAGE_PHOTO_DEST'] = 'images/stages/'
app.config['GET_STAGE_PHOTO_DEST'] = 'static/'
app.config['STATIC_DEST'] = 'app/static/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


class StageService():

	def allowed_file(self, filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

	def urlHelper(self, url):
		return request.url_root + app.config['GET_STAGE_PHOTO_DEST'] + url

	def get(self):
		stages = db.session.query(Stage).all()
		return stages

	def getPictures(self, stage_id):
		stage_pictures = BaseModel.as_list(db.session.query(StagePhotos).filter_by(stage_id=stage_id).all())
		for stage_picture in stage_pictures:
			stage_picture['url'] = self.urlHelper(stage_picture['url'])
		return stage_pictures

	def show(self, id):
		stage = db.session.query(Stage).filter_by(id=id).first()
		return stage

	def showPicture(self, stage_id, id):
		stage_picture = db.session.query(StagePhotos).filter_by(stage_id=stage_id).filter_by(id=id).first().as_dict()
		stage_picture['url'] = self.urlHelper(stage_picture['url'])
		return stage_picture

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
		ext = (file.filename.rsplit('.', 1)[1])
		if file and self.allowed_file(file.filename):
			filename = secure_filename(file.filename)
			now = datetime.datetime.now()
			filename = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '.' + ext
			file.save(os.path.join(app.config['POST_STAGE_PHOTO_DEST'], filename))
			self.model_stage_picture = StagePhotos()
			self.model_stage_picture.stage_id = payloads['stage_id']
			self.model_stage_picture.url = app.config['SAVE_STAGE_PHOTO_DEST'] + filename
			db.session.add(self.model_stage_picture)
			try:
				db.session.commit()
				data = self.model_stage_picture.as_dict()
				data['url'] = self.urlHelper(data['url'])
				print(data)
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

	def updatePicture(self, payloads, stage_id, id):
		try:
			self.model_stage_picture = db.session.query(StagePhotos).filter_by(stage_id=stage_id).filter_by(id=id)
			self.url = self.model_stage_picture.first().url
			os.remove(app.config['STATIC_DEST'] + self.url)
			file = request.files['image_file']
			ext = (file.filename.rsplit('.', 1)[1])
			if file and self.allowed_file(file.filename):
				filename = secure_filename(file.filename)
				now = datetime.datetime.now()
				filename = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '.' + ext
				file.save(os.path.join(app.config['POST_STAGE_PHOTO_DEST'], filename))
				self.model_stage_picture.update({
					'url': app.config['SAVE_STAGE_PHOTO_DEST'] + filename,
					'updated_at': datetime.datetime.now()
				})
				db.session.commit()
				data = self.model_stage_picture.first().as_dict()
				data['url'] = self.urlHelper(data['url'])
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

	def deletePicture(self, stage_id, id):
		self.model_stage_picture = db.session.query(StagePhotos).filter_by(stage_id=stage_id).filter_by(id=id)
		self.url = self.model_stage_picture.first().url
		if self.model_stage_picture.first() is not None:
			# delete row
			os.remove(app.config['STATIC_DEST'] + self.url)
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
