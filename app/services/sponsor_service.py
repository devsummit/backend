import os
import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from app.configs.constants import SPONSOR_STAGES, SPONSOR_TYPES
# import model class
from app.models.sponsor import Sponsor
from app.models.sponsor_templates import SponsorTemplate
from app.models.sponsor_interaction_log import SponsorInteractionLog
from app.services.base_service import BaseService
from app.models.base_model import BaseModel
from app.builders.response_builder import ResponseBuilder
from sqlalchemy import and_
from flask import current_app
from PIL import Image
from app.configs.constants import IMAGE_QUALITY
from app.services.helper import Helper 
from werkzeug import secure_filename


class SponsorService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def get(self, request):
        self.total_items = Sponsor.query.count()

        if request.args.get('page'):
            self.page = request.args.get('page')
        else:
            self.perpage = self.total_items
            self.page = 1
        self.base_url = request.base_url
        # paginate
        paginate = super().paginate(db.session.query(Sponsor))
        paginate = super().transform()
        response = ResponseBuilder()
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        for entry in result['data']:
            if entry['attachment']:
                entry['attachment'] = Helper().url_helper(entry['attachment'], current_app.config['GET_DEST'])
            else:
                entry['attachment'] = "https://museum.wales/media/40374/thumb_480/empty-profile-grey.jpg"
        return result

    def get_logs(self, id):
        response = ResponseBuilder()
        logs = db.session.query(SponsorInteractionLog).filter_by(sponsor_id=id).all()
        return response.set_data(BaseModel.as_list(logs)).build()

    def post_log(self, payload, id):
        response = ResponseBuilder()
        log = SponsorInteractionLog()
        log.description = payload['description']
        log.sponsor_id = id
        db.session.add(log)
        try:
            db.session.commit()
            return response.set_data(log.as_dict()).set_message('logged').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def show(self, id):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id).first()
        data = sponsor.as_dict() if sponsor else None
        if data:
            return response.set_data(data).build()
        return response.set_error(True).set_message('data not found').set_data(None).build()

    def create(self, payload):
        response = ResponseBuilder()
        attachment = self.save_file(payload['attachment']) if payload['attachment'] is not None else None
        sponsor = Sponsor()
        sponsor.name = payload['name']
        sponsor.phone = payload['phone']
        sponsor.email = payload['email']
        sponsor.note = payload['note']
        sponsor.stage = str(payload['stage']) if payload['stage'] else '1'  # default to one as lead
        sponsor.type = str(payload['type']) or '4' if sponsor.stage == '3' else None  # default to four if stage is official
        sponsor.attachment = attachment
        db.session.add(sponsor)

        try:
            db.session.commit()
            #add sponsor_template
            if payload['stage'] == 3:
                sponsor = db.session.query(Sponsor).filter_by(stage=3).order_by(desc(Sponsor.id)).first()
                sponsor_template = SponsorTemplate()
                sponsor_template.sponsor_id = sponsor.id
                db.session.add(sponsor_template)
                db.session.commit()
            return response.set_data(sponsor.as_dict()).set_message('Data created succesfully').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def update(self, id, payload):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id)
        data = sponsor.first().as_dict() if sponsor.first() else None
        if data['attachment'] is not None and payload['attachment']:
                os.remove(current_app.config['STATIC_DEST'] + data['attachment'])
        if data is None:
            return response.set_error(True).set_message('data not found').set_data(None).build()
        if data['stage'] != payload['stage']:
            log = SponsorInteractionLog()
            _from = SPONSOR_STAGES[data['stage']] if data['stage'] else 'None'
            _to = SPONSOR_STAGES[str(payload['stage'])] if payload['stage'] else 'None'
            log.description = 'Admin move stage from: ' + _from + ' to: ' + _to
            log.sponsor_id = id
            db.session.add(log)

        if (data['type'] != payload['type']):
            log = SponsorInteractionLog()
            _from = SPONSOR_TYPES[data['type']] if data['type'] else 'None'
            _to = SPONSOR_TYPES[str(payload['type'])] if payload['type'] else 'None'
            log.description = 'Admin move stage from: ' + _from + ' to: ' + _to
            log.sponsor_id = id
            db.session.add(log)

        new_data = super().filter_update_payload(payload)

        if SPONSOR_STAGES[str(payload['stage'])] is not SPONSOR_STAGES['3']:
            new_data['type'] = None
        if payload['attachment']:
            attachment = self.save_file(payload['attachment']) if payload['attachment'] is not None else None
            new_data['attachment'] = attachment
        new_data['updated_at'] = datetime.datetime.now()
        sponsor.update(new_data)
        try:
            db.session.commit()
            #when update sponsor to official, automatically create sponsor_template
            if new_data['stage'] == 3:
                sponsor_update = Sponsor()
                sponsor_update = db.session.query(Sponsor).filter(and_(Sponsor.stage == 3, Sponsor.id == id)).first()
                sponsor_template = SponsorTemplate()
                sponsor_template.sponsor_id = sponsor_update.id
                db.session.add(sponsor_template)
                db.session.commit()
            return response.set_data(sponsor.first().as_dict()).build()

        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def delete(self, id):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id)
        if sponsor.first():
            sponsor_dict = sponsor.first().as_dict()
            if sponsor_dict['attachment'] is not None:
                os.remove(current_app.config['STATIC_DEST'] + sponsor_dict['attachment'])
            sponsor.delete()
            db.session.commit()
            return response.set_message('data deleted').set_data(None).build()
        return response.set_message('data not found').set_error(True).build()

    def save_file(self, file, id=None):
        image = Image.open(file, 'r')
        if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            if (Helper().allowed_file(file.filename, ['jpg', 'jpeg', 'png'])):
                image = image.convert("RGB")
            filename = secure_filename(file.filename)
            filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
            image.save(os.path.join(current_app.config['POST_SPONSOR_PIC_DEST'], filename), quality=IMAGE_QUALITY, optimize=True)
            return current_app.config['SAVE_SPONSOR_PIC_DEST'] + filename
        else:
            return None
