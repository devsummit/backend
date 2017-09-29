from app.models import db
from flask import Flask, request, current_app  # noqa
import os
from app.services.helper import Helper
# import model class
from app.models.booth_gallery import BoothGallery
from app.models.booth import Booth
from app.models.base_model import BaseModel
from app.builders.response_builder import ResponseBuilder


class BoothGalleryService():

    def index(self):
        response = ResponseBuilder()
        booth_galleries = BaseModel.as_list(db.session.query(BoothGallery).all())
        if booth_galleries is not None:
            for booth_gallery in booth_galleries:
                booth_gallery = booth_gallery
                booth_id = booth_gallery['booth_id']
                booth_gallery['url'] = Helper().url_helper(booth_gallery['url'], current_app.config['GET_DEST'])
        booth = db.session.query(Booth).filter_by(id=booth_id).first().as_dict()
        booth['logo_url'] = Helper().url_helper(booth['logo_url'], current_app.config['GET_DEST']) if booth['logo_url'] else "https://museum.wales/media/40374/thumb_480/empty-profile-grey.jpg"
        return response.set_data(booth_galleries).set_message('data retrieved successfully').set_included(booth).build()

    def show(self, id):
        reponse = ResponseBuilder()
        booth_galleries = db.session.query(BoothGallery).filter_by(booth_id=id).all()
        result = []
        if booth_galleries is not None:
            for booth_gallery in booth_galleries:
                booth_gallery = booth_gallery.as_dict()
                booth_gallery['url'] = Helper().url_helper(booth_gallery['url'], current_app.config['GET_DEST'])
                result.append(booth_gallery)
        return reponse.set_data(result).set_message('data retrieved successfully').build()

    def self_gallery(self, booth_id):
        response = ResponseBuilder()
        booth_galleries = BaseModel.as_list(db.session.query(BoothGallery).filter_by(booth_id=booth_id).all())
        if booth_galleries is not None:
            for booth_gallery in booth_galleries:
                booth_gallery = booth_gallery
                booth_gallery['url'] = Helper().url_helper(booth_gallery['url'], current_app.config['GET_DEST'])

            return response.set_data(booth_galleries).set_message('data retieved successfully').build()
        else:
            return response.set_error(True).set_data(None).set_message('data not found').build()

    def booth_gallery(self, booth_id):
        response = ResponseBuilder()
        booth_galleries = db.session.query(BoothGallery).filter_by(booth_id=booth_id).all()
        if booth_galleries is not None:
            for booth_gallery in booth_galleries:
                booth_gallery = booth_gallery
                booth_gallery['url'] = Helper().url_helper(booth_gallery['url'], current_app.config['GET_DEST'])
                
            return response.set_data(booth_galleries).set_message('data retrieved sucessfully').build()
        else:
            return response.set_data(None).set_message('data not found').set_error(True).build()

    def create(self, payloads):
        response = ResponseBuilder()
        booth_id = payloads['booth_id']
        files = payloads['image_files']

        check = self.check_files(files)
        if not check:
            return response.set_error(True).set_message('one or more files are not in correct format').build()
        else:
            results = []
            for file in files:
                self.model_booth_gallery = BoothGallery()
                db.session.add(self.model_booth_gallery)
                success = True
                try:
                    file_name = Helper.time_string() + "_" + file.filename
                    file.save(os.path.join(current_app.config['POST_BOOTH_GALL_DEST'], file_name))
                    self.model_booth_gallery.url = current_app.config['SAVE_BOOTH_GALL_DEST'] + file_name
                    self.model_booth_gallery.booth_id = booth_id
                    db.session.commit()
                    data = self.model_booth_gallery.as_dict()
                    data['url'] = Helper().url_helper(data['url'], current_app.config['GET_DEST'])
                    results.append(data)
                except:
                    success = False
            
            if success:
                return response.set_data(results).set_message('upload success').build()
            else:
                return response.set_error(True).set_message('some files can not be uploaded').set_data(None).build()

    def delete(self, id):
        response = ResponseBuilder()
        self.model_booth_gallery = db.session.query(BoothGallery).filter_by(id=id)
        if self.model_booth_gallery.first() is not None:
            # delete file
            os.remove(current_app.config['STATIC_DEST'] + self.model_booth_gallery.first().url)
            # delete row
            self.model_booth_gallery.delete()
            db.session.commit()
            return response.set_message('data deleted successfully').set_error(False).build()
        else:
            return response.set_message('data not found').set_error(True).build()

    def check_files(self, files):
        for file in files:
            if not Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                return False
        return True

