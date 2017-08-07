from seeders.role_seeder import RoleSeeder
from seeders.events_seeder import EventsSeeder


class Seed():

	@staticmethod
	def run():
		print('seeding roles...')
		RoleSeeder.run()
		print('finish seeding roles')

		print('seeding events...')
		EventsSeeder.run()
		print('finish seeding events')
