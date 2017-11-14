import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from flask import json, jsonify
# import model class
from app.models.questioner import Questioner
from app.models.booth import Booth
from app.models.questioner_answer import QuestionerAnswer


class QuestionerService():
    def get(self):
        questioners = db.session.query(Questioner).all()
        _results = []
        for questioner in questioners:
            data = questioner.as_dict()
            data['booth'] = questioner.booth.as_dict()
            _results.append(data)
        return _results
        
    def show(self, id):
        questioner = db.session.query(Questioner).filter_by(id=id).first()
        data = questioner.as_dict() if questioner else None
        if data:
            data['booth'] = questioner.booth.as_dict()
        return data 

    def patch(self, id, payload):
        try:
            if id==None:
                questioner = Questioner()
                questioner.questions = json.dumps(payload['questions'])
                booth = None
                if payload['booth_id']:
                    questioner.booth_id = payload['booth_id']
                else:
                    booth = db.session.query(Booth).first()
                    questioner.booth_id = booth.id
                db.session.add(questioner)
            else:
                questioner = db.session.query(Questioner).filter_by(id=id)
                if questioner.first():
                    questioner.update({
                        'booth_id': payload['booth_id'],
                        'questions': json.dumps(payload['questions'])    
                    })
                    questioner = questioner.first()
                else:
                    return {
                        'error': True,
                        'data': 'not found'
                    }
            db.session.commit()
            return {
                'error': False,
                'data': questioner.as_dict(),
                'message': 'questioner succesfully posted'
            }
        except SQLAlchemyError as e:
            return {
                'error': True,
                'data': None,
                'message': e.orig.args
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
