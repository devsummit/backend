from faker import Faker
from datetime import timedelta
from app.models.events import Events
from app.models import db

'''
Seeder class for
'''


class EventsSeeder():

    @staticmethod
    def run():
        """
        Create 10 Event seeds
        """
        fake = Faker()
        for i in range(0, 10):
            time_start = fake.future_datetime(end_date="+30d", tzinfo=None)
            time_end = time_start + timedelta(hours=3)
            information = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None)
            event = {
                'information': information,
                'time_start': time_start,
                'time_end': time_end
            }

            new_event = Events()
            new_event.information = event['information']
            new_event.time_start = event['time_start']
            new_event.time_end = event['time_end']
            db.session.add(new_event)
            db.session.commit()
