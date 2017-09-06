from app.models.event import Event
from app.models import db

'''
Seeder class for
'''


class EventsSeeder():

    @staticmethod
    def run():
        """
        Create 4 Event seeds
        """
        speak_event = Event()
        speak_event.information = 'Speaking about javascript frameworks: Vue, React, and Angular'
        speak_event.user_id = 4
        speak_event.title = 'Javascript Frameworks'
        speak_event.type = 'speaker'
        db.session.add(speak_event)

        speak_b_event = Event()
        speak_b_event.information = 'Speaking about Native Java / Kotlin vs React-native'
        speak_b_event.user_id = 4
        speak_b_event.title = 'Mobile Software development'
        speak_b_event.type = 'speaker'
        db.session.add(speak_b_event)

        hackaton_a_event = Event()
        hackaton_a_event.information = 'PHP Indonesia Group, Contributing library to the world'
        hackaton_a_event.title = 'PHP Library Hackaton'
        hackaton_a_event.type = 'hackaton'
        db.session.add(hackaton_a_event)

        booth_event = Event()
        booth_event.information = 'Github'
        booth_event.title = 'Github Booth'
        booth_event.type = 'booth'
        db.session.add(booth_event)
        db.session.commit()
