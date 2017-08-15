from faker import Faker
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.stage import Stage
from app.models.booth import Booth
from app.models import db
from random import randint
import random

'''
Seeder class for
'''


class BoothsSeeder():

    @staticmethod
    def run():
        """
        Create 10 Booths seeds
        """
        fake = Faker()
        users = BaseModel.as_list(db.session.query(User).all())
        stages = BaseModel.as_list(db.session.query(Stage).all())
        for i in range(1, 10):
            points = randint(0, 1000)
            summary = fake.sentence(
                nb_words=10, variable_nb_words=True, ext_word_list=None
            )
            new_booth = Booth()
            new_booth.user_id = random.choice(users)['id']
            new_booth.stage_id = random.choice(stages)['id']
            new_booth.points = points
            new_booth.summary = summary
            db.session.add(new_booth)
            db.session.commit()
