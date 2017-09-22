# manage.py

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean

# configuration
from app.configs import settings
from app import create_app

manager = Manager(create_app(settings))

# add executeable command 
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())

# Seeder
from seeders.seed import Seed
from seeders.production_seed import ProductionSeed

@manager.command
def seed():
    Seed.run()
@manager.command
def productionseed():
    ProductionSeed.run()


if __name__ == "__main__":
    manager.run()
