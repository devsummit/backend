import datetime
import os
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from PIL import Image
from flask import current_app
from app.configs.constants import IMAGE_QUALITY
from app.services.helper import Helper
from werkzeug import secure_filename
# import model class
from app.models.sponsor_templates import SponsorTemplate
from app.models.sponsor import Sponsor
from app.services.base_service import BaseService
from app.models.base_model import BaseModel
from app.builders.response_builder import ResponseBuilder

class SponsorTemplateService(BaseService):

    def get(self, request):
        sponsor_templates = db.session.query(SponsorTemplate).all()
        results = []
        for sponsor in sponsor_templates:
            sponsor_data = db.session.query(Sponsor).filter_by(id=sponsor.sponsor_id).first()
            data = sponsor.as_dict()
            data['sponsor'] = sponsor_data.as_dict()
            results.append(data)
        response = ResponseBuilder()
        result = response.set_data(results).build()
        return result

    def show(self, sponsor_id):
        response = ResponseBuilder()
        sponsor_template = db.session.query(SponsorTemplate).filter_by(sponsor_id=sponsor_id).first()
        sponsor = db.session.query(Sponsor).filter_by(id=sponsor_id).first()
        data = {}
        data = sponsor_template.as_dict() if sponsor_template else None
        data['sponsor'] = sponsor.as_dict()
        return response.set_data(data).build()

    def create(self, payloads):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=payloads['sponsor_id']).first()
        sponsor_template = SponsorTemplate()
        sponsor_template.sponsor_id = payloads['sponsor_id']
        sponsor_template.message = payloads['message']
        attachment = self.save_file(payloads['attachment']) if payloads['attachment'] is not None else None
        sponsor_template.attachment = attachment
        sponsor_template.redirect_url = payloads['redirect_url']
        db.session.add(sponsor_template)
        try:
            db.session.commit()
            sponsor = sponsor.as_dict()
            data = sponsor_template.as_dict()
            data['sponsor'] = sponsor
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def update(self, payloads, sponsor_id):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=sponsor_id).first()
        try:
            sponsor_template = db.session.query(SponsorTemplate).filter_by(sponsor_id=sponsor_id)
            sponsor_template.update({
                'message': payloads['message'],
                'redirect_url': payloads['redirect_url']
            })
            if payloads['attachment']:
                attachment = self.save_file(payloads['attachment']) if payloads['attachment'] is not None else None
                sponsor_template.update({
                    'attachment': attachment
                })
            db.session.commit()
            data = sponsor_template.first().as_dict()
            data['sponsor'] = sponsor.as_dict()
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