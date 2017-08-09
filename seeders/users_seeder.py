from faker import Faker
from datetime import timedelta
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
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.safe_email()
            username = fake.user_name()
            password = fake.md5(raw_output=False)
            role_id = randint(1,4)
            user = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'password': password,
                'role_id': role_id
            }   
            new_user = User()
            new_user.first_name = user['first_name']
            new_user.last_name = user['last_name']
            new_user.email = user['email']
            new_user.username = user['username']
            new_user.password = user['password']
            new_user.role_id = user['role_id']
            db.session.add(new_user)
            db.session.commit()
