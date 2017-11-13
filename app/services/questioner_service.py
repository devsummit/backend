import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.questioner import Questioner


class QuestionerService():
    def get(self):
        return db.session.query(Questioner).all()
        
    def show(self, id):
        questioner = db.session.query(Questioner).filter_by(id=id).first()
        data = questioner.as_dict() if questioner else None
        return data 

    def patch(self, id, payload):
        try:
            questioner = db.session.query(Questioner).filter_by(id=id)
            if questioner.first():
                questioner.update({
                    'questions': payload['questions']    
                })
            else:
                questioner = Questioner()
                questioner.questions = payloads['questions']
                db.session.add(questioner)
            db.session.commit()
            data = questioner.first().as_dict()
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
