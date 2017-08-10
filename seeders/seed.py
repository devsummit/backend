from seeders.role_seeder import RoleSeeder
from seeders.users_seeder import UsersSeeder
from seeders.stages_seeder import StagesSeeder
from seeders.events_seeder import EventsSeeder
from seeders.beacons_seeder import BeaconsSeeder
from seeders.schedules_seeder import SchedulesSeeder
from seeders.tickets_seeder import TicketsSeeder
from seeders.user_tickets_seeder import UserTicketsSeeder
from seeders.ticket_transfer_logs_seeder import TicketTransferLogsSeeder


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

		print('seeding tickets...')
		TicketsSeeder.run()
		print('finish seeding tickets')

		print('seeding user_ticket ...')
		UserTicketsSeeder.run()
		print('finish seeding user_ticket')

		print('seeding ticket transfer logs...')
		TicketTransferLogsSeeder.run()
		print('finish seeding ticket transfer logs')
