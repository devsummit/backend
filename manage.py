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


@manager.command
def seed():
    Seed.run()


if __name__ == "__main__":
    manager.run()
