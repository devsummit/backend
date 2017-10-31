import datetime
from app.controllers.base_controller import BaseController
from sqlalchemy.exc import SQLAlchemyError
from app.models.partner_pj import PartnerPj 
from app.models.partners import Partner
from app.configs.constants import ROLE
from app.models.user import User
from app.models import db


class PartnerPjController(BaseController):
	
	@staticmethod
	def grant(request):
		user_id = request.json['user_id'] if 'user_id' in request.json else None
		partner_id = request.json['partner_id'] if 'partner_id' in request.json else None
		if user_id is None or partner_id is None:
			return BaseController.send_response_api(None, 'invalid payload')
		result = db.session.query(PartnerPj).filter_by(partner_id=partner_id)
		if result.first() is None:
			partner = db.session.query(Partner).filter_by(id=partner_id).first()
			if partner:
				newPartnerPj = PartnerPj()
				newPartnerPj.user_id = user_id
				newPartnerPj.partner_id = partner_id
				db.session.add(newPartnerPj)
				try:
					db.session.commit()
					return BaseController.send_response_api(None, 'pj updated')
				except SQLAlchemyError as e:
					return BaseController.send_error_api(None, 'query error occured')
			else:
				return BaseController.send_error_api(None, 'partner not found')
		# revert user role
		user = db.session.query(User).filter_by(id=result.first().user_id).update({
				'role_id': ROLE['user']
			})
		result.update({
			'user_id': user_id,
			'updated_at': datetime.datetime.now()
		})
		try:
			db.session.commit()
			new_user = db.session.query(User).filter_by(id=user_id).update({
					'role_id': ROLE['partner'],
					'updated_at': datetime.datetime.now()
				})
			db.session.commit()
			return BaseController.send_response_api(None, 'pj updated')
		except SQLAlchemyError as e:
			return BaseController.send_error_api(None, 'query error occured')
