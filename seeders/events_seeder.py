from faker import Faker
from app.models.event import Event
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
            title = fake.sentence(
                nb_words=3, variable_nb_words=True, ext_word_list=None)
            information = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None)
            event = {
                'information': information,
                'title': title
            }

            new_event = Event()
            new_event.information = event['information']
            new_event.title = event['title']
            db.session.add(new_event)
            db.session.commit()
