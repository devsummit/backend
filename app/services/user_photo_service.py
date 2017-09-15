import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from flask import request, current_app
from app.configs.constants import ROLE
from app.services.helper import Helper 
import os
# import model class
from app.models.user_photo import UserPhoto
from app.models.base_model import BaseModel
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class UserPhotoService(BaseService):

    def get(self):
        user_photos = BaseModel.as_list(db.session.query(UserPhoto).all())
        for user_photo in user_photos:
            user_photo['url'] = Helper().url_helper(user_photo['url'], current_app.config['GET_DEST'])
        return user_photos

    def show(self, user_id):
        user_photo = db.session.query(UserPhoto).filter_by(user_id=user_id).first()
        if(user_photo is None):
            data = {
                'photo_exist': False
            }
            return {
                'data': data,
                'error': True,
                'message': 'User Photo is not found'
            }    
        user_photo = user_photo.as_dict()
        user_photo['url'] = Helper().url_helper(user_photo['url'], current_app.config['GET_DEST'])
        return {
            'data': user_photo,
            'error': False,
            'message': 'photo retrieved successfully'
        }

    def create(self, payloads):
        response = ResponseBuilder()
        user_id = payloads['user_id']
        is_exist = db.session.query(UserPhoto).filter_by(user_id=user_id).first()
        if(is_exist is not None):
            return self.update(payloads)
        file = request.files['image_data']
        if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            self.model_user_photo = UserPhoto()
            db.session.add(self.model_user_photo)
            try:
                filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
                file.save(os.path.join(current_app.config['POST_USER_PHOTO_DEST'], filename))
                self.model_user_photo.url = current_app.config['SAVE_USER_PHOTO_DEST'] + filename
                self.model_user_photo.user_id = user_id
                db.session.commit()

                data = self.model_user_photo.first().user.include_photos().as_dict()
                data = self.include_user_role(data)
                return response.set_data(data).set_message('photo saved').build()
            except SQLAlchemyError as e:
                data = e.orig.args
                return response.set_error(True).set_data(None).set_message(data).build()

    def include_user_role(self, user):
        if (user['role_id'] is ROLE['speaker']):
            user = super().outer_include(user, ['Speaker'])
        elif (user['role_id'] is ROLE['booth']):
            user = super().outer_include(user, ['Booth'])
        elif (user['role_id'] is ROLE['attendee']):
            user = super().outer_include(user, ['Attendee'])
        return user

    def update(self, payloads):
        response = ResponseBuilder()
        user_id = payloads['user_id']
        file = request.files['image_data']
        if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            try:
                filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
                file.save(os.path.join(current_app.config['POST_USER_PHOTO_DEST'], filename))
                newUrl = current_app.config['SAVE_USER_PHOTO_DEST'] + filename
                self.model_user_photo = db.session.query(UserPhoto).filter_by(user_id=user_id)
                self.user_photo = db.session.query(UserPhoto).filter_by(user_id=user_id).first()
                os.remove(current_app.config['STATIC_DEST'] + self.user_photo.url)
                self.model_user_photo.update({
                    'url': newUrl,
                    'updated_at': datetime.datetime.now()
                })
                db.session.commit()
                data = self.model_user_photo.first().user.include_photos().as_dict()
                data = self.include_user_role(data)

                return response.set_data(data).set_message('user photo updated').build()
            except SQLAlchemyError as e:
                data = e.orig.args
                return response.set_error(True).set_data(None).set_message(data).build()

    def delete(self, user_id):
        self.model_user_photo = db.session.query(UserPhoto).filter_by(user_id=user_id)
        if self.model_user_photo.first() is not None:
            # delete file
            os.remove(current_app.config['STATIC_DEST'] + self.model_user_photo.first().url)
            # delete row
            self.model_user_photo.delete()
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
