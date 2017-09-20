from seeders.role_seeder import RoleSeeder
from seeders.users_seeder import UsersSeeder
from seeders.tickets_seeder import TicketsSeeder
from seeders.clients_seeder import ClientsSeeder


class ProductionSeed():

	@staticmethod
	def run():
		print('seeding roles...')
		RoleSeeder.run()
		print('finish seeding roles')

		print('seeding users...')
		UsersSeeder.run()
		print('finish seeding users')

		print('seeding tickets...')
		TicketsSeeder.run()
		print('finish seeding tickets')

		print('seeding client...')
		ClientsSeeder.run()
		print('finish seeding client')
