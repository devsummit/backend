import os
import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from app.models.package_management import PackageManagement

class PackageManagementService(BaseService):

	def get(self, request):
		package_managements = db.session.query(PackageManagement).all()
		results = []
		for package in package_managements:
			data = package.as_dict()
			results.append(data)
		response = ResponseBuilder()
		result = response.set_data(results).build()
		return result

	def create(self, payloads):
		response = ResponseBuilder()
		package_managements = PackageManagement()
		package_managements.name = payloads['name']
		package_managements.price = payloads['price']
		package_managements.quota = payloads['quota']
		db.session.add(package_managements)
		try:
			db.session.commit()
			data = package_managements.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def show(self, id):
		response = ResponseBuilder()
		packagemanagement = db.session.query(PackageManagement).filter_by(id=id).first()
		data = packagemanagement.as_dict() if packagemanagement else None
		if data:
			return response.set_data(data).build()
		return response.set_error(True).set_message('data not found').set_data(None).build()

	def update(self, id, payloads):
		response = ResponseBuilder()
		try:
			packagemanagement = db.session.query(PackageManagement).filter_by(id=id)			
			packagemanagement.update({
				'name': payloads['name'],
				'price': payloads['price'],
				'quota': payloads['quota'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = packagemanagement.first()
			return response.set_data(data.as_dict()).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).build()

	def delete(self, id):
		response = ResponseBuilder()
		packagemanagement = db.session.query(PackageManagement).filter_by(id=id)
		if packagemanagement.first() is not None:
			packagemanagement.delete()
			db.session.commit()
			return response.set_message('Package entry was deleted').build()
		else:
			data = 'Entry not found'
			return response.set_data(None).set_message(data).set_error(True).build()