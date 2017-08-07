from app.models.role import Role
from app.models import db

'''
Seeder class for 
'''


class RoleSeeder():

	@staticmethod
	def run():
		roles = ('admin', 'attendee', 'booth', 'speaker')
		for role in roles:
			new_role = Role()
			new_role.name = role
			db.session.add(new_role)
			db.session.commit()
