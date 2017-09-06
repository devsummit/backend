from faker import Faker
from datetime import timedelta
from app.models.schedule import Schedule
from app.models import db

'''
Seeder class for
'''


class SchedulesSeeder():

    @staticmethod
    def run():
        """
        Create 1 Schedules seeds
        """
        fake = Faker()
        new_schedule = Schedule()
        new_schedule.event_id = 1
        new_schedule.stage_id = 1
        new_schedule.time_start = fake.future_datetime()
        new_schedule.time_end = new_schedule.time_start + timedelta(hours=1)
        db.session.add(new_schedule)
        db.session.commit()
