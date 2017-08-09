from faker import Faker
from app.models.user import User
from app.models import db
from random import randint

'''
Seeder class for
'''


class UsersSeeder():

    @staticmethod
    def run():
        """
        Create 20 Users seeds
        """
        fake = Faker()
        for i in range(0, 20):
            new_user = User()
            new_user.first_name = fake.first_name()
            new_user.last_name = fake.last_name()
            new_user.email = fake.safe_email()
            new_user.username = fake.user_name()
            new_user.password = fake.md5(raw_output=False)
            new_user.role_id = randint(1, 4)
            db.session.add(new_user)
            db.session.commit()
