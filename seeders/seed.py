from seeders.role_seeder import RoleSeeder
from seeders.users_seeder import UsersSeeder
from seeders.stages_seeder import StagesSeeder
from seeders.events_seeder import EventsSeeder
from seeders.beacons_seeder import BeaconsSeeder
from seeders.schedules_seeder import SchedulesSeeder
from seeders.tickets_seeder import TicketsSeeder
from seeders.clients_seeder import ClientsSeeder
from seeders.payments_seeder import PaymentsSeeder
from seeders.orders_seeder import OrdersSeeder
from seeders.order_details_seeder import OrdersDetailsSeeder
from seeders.user_tickets_seeder import UserTicketsSeeder
from seeders.speaker_candidates_seeder import SpeakerCandidateSeeder


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

		print('seeding orders...')
		OrdersSeeder.run()
		print('finish seeding orders')

		print('seeding client...')
		ClientsSeeder.run()
		print('finish seeding client')

		print('seeding payments...')
		PaymentsSeeder.run()
		print('finish seeding payment')

		print('seeding orderdetailsseeder...')
		OrdersDetailsSeeder.run()
		print('finish seeding Order Details Seeder')

		print('seeding user tickets seeder...')
		UserTicketsSeeder.run()
		print('finish seeding user tickets seeder')

		print('seeding speaker candidates')
		SpeakerCandidateSeeder.run()
		print('finish seeding speaker candidates')
