import datetime
from flask import current_app
from app.models import db
from app.models.hackaton_proposals import HackatonProposal
from app.services.helper import Helper 
from sqlalchemy.exc import SQLAlchemyError
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class HackatonProposalService(BaseService):


	def get(self, status):
		response = ResponseBuilder()
		results = db.session.query(HackatonProposal).filter_by(status=status).all()
		_results = []
		for result in results:
			_results.append(result)
		return response.set_data(_results).build()

	def create(self, payloads):
		response = ResponseBuilder()
		hackaton_proposal = HackatonProposal()
		hackaton_proposal.github_link = payloads['github_link']
		hackaton_proposal.order_id = payloads['order_id']
		hackaton_proposal.status = 'pending'
		db.session.add(hackaton_proposal)
		try:
			db.session.commit()
			return response.set_data(hackaton_proposal.as_dict()).set_message('proposal succesfully created').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()		


	def deny(self, payloads):
		response = ResponseBuilder()
		hackaton_proposal = db.session.query(HackatonProposal).filter_by(id=payloads['id'])
		if hackaton_proposal.first() is None:
			return response.set_error(True).set_data(None).set_message('proposal not found').build()
		hackaton_proposal.update({
			'updated_at': datetime.datetime.now(),
			'status': 'denied'
		})
		try:
			db.session.commit()
			return response.set_data(None).set_message('proposal succesfully denied').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()
