import datetime
from app.controllers.base_controller import BaseController
from sqlalchemy.exc import SQLAlchemyError
from app.models.partner_pj import PartnerPj
from app.models.referal_owner import ReferalOwner
from app.models.referal import Referal
from app.models.partners import Partner
from app.models.order import Order
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
					new_user = db.session.query(User).filter_by(id=user_id).update({
						'role_id': ROLE['partner'],
						'updated_at': datetime.datetime.now()
						})
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

	@staticmethod
	def get_info(user, request):
		result = {}
		partnerpj = db.session.query(PartnerPj).filter_by(user_id=user['id']).first()
		if partnerpj is None:
			return BaseController.send_error_api(None, 'user is not a partner pj')
		referal_owner = db.session.query(ReferalOwner).filter_by(referalable_id=partnerpj.partner.id).first()
		# get referal info
		referal = db.session.query(Referal).filter_by(id=referal_owner.referal_id).first()
		result['partner'] = partnerpj.partner.as_dict()
		# check if referal exist
		included = {}
		if referal:
			result['referal'] = referal.as_dict()
			included['count'] = db.session.query(Order).filter_by(referal_id=referal.id).count()
		else:
			result['referal'] = None
		# get partner info
		return BaseController.send_response_api(result, 'data retrieved', included)


	@staticmethod
	def admin_get_info(referal_id):
		result = {}
		referal = db.session.query(Referal).filter_by(id=referal_id).first()
		if referal is None:
			return BaseController.send_error_api(None, 'referal not found')
		referal_owner = db.session.query(ReferalOwner).filter_by(referal_id=referal_id).first()
		partner = db.session.query(Partner).filter_by(id=referal_owner.referalable_id).first()

		response = {}
		response['data'] = {}
		response['data']['partner'] = partner.as_dict()
		response['data']['referal'] = referal.as_dict()
		response['included'] = {}
		response['included']['count'] = db.session.query(Order).filter_by(referal_id=referal.id).count()
		response['links'] = {}
		response['meta'] = {}
		response['meta']['message'] = 'data retrieved'
		response['meta']['success'] = 'true' 
		return response
		# return BaseController.send_response_api(result, 'data retrieved', included)
