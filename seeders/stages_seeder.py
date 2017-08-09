from faker import Faker
from app.models.stage import Stage
from app.models import db
import random

'''
Seeder class for
'''


class StagesSeeder():

    @staticmethod
    def run():
        """
        Create 20 Users seeds
        """
        fake = Faker()
        stage_types = ['podium', 'booth', 'mainstage']
        for i in range(0, 10):
            name = fake.name()
            stage_type = random.choice(stage_types)
            information = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None)
            stage = {
                'name': name,
                'stage_type': stage_type,
                'information': information
            }     
            new_stage = Stage()
            new_stage.name = stage['name']
            new_stage.stage_type = stage['stage_type']
            new_stage.information = stage['information']
            db.session.add(new_stage)
            db.session.commit()
