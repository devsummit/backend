import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.questioner import Questioner
from app.models.questioner_answer import QuestionerAnswer


class QuestionerService():
    def get(self):
        return db.session.query(Questioner).all()
        
    def show(self, id):
        questioner = db.session.query(Questioner).filter_by(id=id).first()
        data = questioner.as_dict() if questioner else None
        return data 

    def patch(self, id, payload):
        try:
            if id==None:
                questioner = Questioner()
                questioner.questions = payload['questions']
                questioner.booth_id = payload['booth_id']
                db.session.add(questioner)
                data = questioner.as_dict()
            else:
                questioner = db.session.query(Questioner).filter_by(id=id)
                if questioner.first():
                    questioner.update({
                        'questions': payload['questions']    
                    })
                    data = questioner.first().as_dict()
                else:
                    return {
                        'error': True,
                        'data': 'not found'
                    }
            db.session.commit()
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

    def post_answer(self, id, user_id, payload):
        try:
            answer = db.session.query(QuestionerAnswer).filter_by(id=id, user_id=user_id)
            if not answer.first():
                answer = QuestionerAnswer()
                answer.user_id = user_id
                answer.questioner_id = id
                answer.answers = payload['answers']
                db.session.add(answer)
                data = answer.as_dict()
            else:
                answer.update({
                    'answers': payload['answers']    
                })
                data = answer.first().as_dict()
            db.session.commit()
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
