from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder
# import model class
from app.models.hacker_team import HackerTeam
from app.models.user import User
from app.models.hacker import Hacker

class HackTeamService():

	def get(self):
		response = ResponseBuilder()
		teams = db.session.query(HackerTeam).all()
		results = []
		for team in teams:
			data = team.as_dict()
			hackers = db.session.query(Hacker).filter_by(team_id=data['id'])
			data['users'] = []
			for hacker in hackers.all():
				include_hacker = hacker.as_dict()
				temp = {}
				temp = hacker.user.as_dict()
				temp['hacker'] = include_hacker
				data['users'].append(temp)
			results.append(data)
		return response.set_data(results).build()

	def show(self, id):
		response = ResponseBuilder()
		team = db.session.query(HackerTeam).filter_by(id=id).first()
		team = team.as_dict() if team else None
		if team is not None:
			hackers = db.session.query(Hacker).filter_by(team_id=team['id'])
			team['users'] = []
			for hacker in hackers.all():
				include_hacker = hacker.as_dict()
				temp = {}
				temp = hacker.user.as_dict()
				temp['hacker'] = include_hacker
				team['users'].append(temp)
		return response.set_data(team).build()

	def create(self, payload, user_id):
		# check if have team
		response = ResponseBuilder()
		hacker = db.session.query(Hacker).filter_by(user_id=user_id)
		if hacker.first().as_dict()['team_id'] is not None:
			return response.set_error(True).set_data(None).set_message('You already have a team').build()
		team_exist = db.session.query(HackerTeam).filter_by(team_name=payload['team_name']).first()
		if team_exist is not None:
			return response.set_error(True).set_data(None).set_message('Team name already taken').build()
		hackerteam = HackerTeam()
		hackerteam.team_name = payload['team_name']
		hackerteam.project_name = payload['project_name']
		db.session.add(hackerteam)
		db.session.commit()
		hacker.update({
			'lead': True,
			'team_id': hackerteam.id
		})
		db.session.commit()
		return response.set_data(hackerteam.as_dict()).set_message('team successfully created').build()

	def delete(self, id):
		response = ResponseBuilder()
		hacker = db.session.query(Hacker).filter_by(team_id=id)
		hacker.update({
			'team_id': None
		})
		db.session.commit()
		hackerteam = db.session.query(HackerTeam).filter_by(id=id)
		hackerteam.delete()
		try:
			db.session.commit()
			return response.set_data(None).set_message('data deleted successfully').build()			
		except SQLAlchemyError as e:
			message = e.orig.args
			return response.set_error(True).set_data(None).set_message(data).build()
