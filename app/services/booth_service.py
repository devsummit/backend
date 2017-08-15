from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.booth import Booth


class BoothService():

    def get(self):
        booths = db.session.query(Booth).all()
        # add included
        included = self.get_includes(booths)
        return {
            'data': booths,
            'included': included
        }

    def show(self, id):
        booth = db.session.query(Booth).filter_by(id=id).first()
        return booth

    def update(self, payloads, id):
        try:
            self.model_booth = db.session.query(Booth).filter_by(id=id)
            self.model_booth.update({
                'user_id': payloads['user_id'],
                'stage_id': payloads['stage_id'],
                'points': payloads['points'],
                'summary': payloads['summary']
            })
            db.session.commit()
            data = self.model_booth.first().as_dict()
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

    def create(self, payloads):
        self.model_booth = Booth()
        self.model_booth.user_id = payloads['user_id']
        self.model_booth.stage_id = payloads['stage_id']
        self.model_booth.points = payloads['points']
        self.model_booth.summary = payloads['summary']
        db.session.add(self.model_booth)
        try:
            db.session.commit()
            data = self.model_booth.as_dict()
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

    def get_includes(self, booths):
        included = []
        if isinstance(booths, list):
            for booth in booths:
                temp = {}
                temp['user'] = booth.user.as_dict()
                temp['stage'] = booth.stage.as_dict()
                included.append(temp)
        else:
            temp = {}
            temp['user'] = booths.user.as_dict()
            temp['stage'] = booths.stage.as_dict()
            included.append(temp)
        return included
