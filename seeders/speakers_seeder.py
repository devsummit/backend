from faker import Faker
from datetime import timedelta
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.speaker import Speaker
from app.models import db
import random

'''
Seeder class for
'''


class SpeakersSeeder():

    @staticmethod
    def run():
        """
        Create 10 Speakers seeds
        """
        fake = Faker()
        users = BaseModel.as_list(db.session.query(User).all())
        for i in range (0, 10):
            job = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None
            )
            summary = fake.sentence(
                nb_words=15, variable_nb_words=True, ext_word_list=None
            )
            information = fake.sentence(
                nb_words=8, variable_nb_words=True, ext_word_list=None
            )
            new_speaker = Speaker()
            new_speaker.user_id = random.choice(users)['id']
            new_speaker.job = job
            new_speaker.summary = summary
            new_speaker.information = information
            db.session.add(new_speaker)
            db.session.commit()
