from seeders.role_seeder import RoleSeeder
from seeders.users_seeder import UsersSeeder
from seeders.stages_seeder import StagesSeeder
from seeders.events_seeder import EventsSeeder
from seeders.beacons_seeder import BeaconsSeeder
from seeders.schedules_seeder import SchedulesSeeder
from seeders.tickets_seeder import TicketsSeeder


class Seed():

	@staticmethod
	def run():
		print('seeding roles...')
		RoleSeeder.run()
		print('finish seeding roles')

		print('seeding users...')
		UsersSeeder.run()
		print('finish seeding users')

		print('seeding stages...')
		StagesSeeder.run()
		print('finish seeding stages')

		print('seeding events...')
		EventsSeeder.run()
		print('finish seeding events')

		print('seeding beacons...')
		BeaconsSeeder.run()
		print('finish seeding beacons')

		print('seeding schedules...')
		SchedulesSeeder.run()
		print('finish seeding schedules')

		print('seeding schedules...')
		TicketsSeeder.run()
		print('finish seeding schedules')