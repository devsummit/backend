from faker import Faker
from datetime import timedelta
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.schedule import Schedule
from app.models.event import Event
from app.models.stage import Stage
from app.models import db
import random

'''
Seeder class for
'''


class SchedulesSeeder():

    @staticmethod
    def run():
        """
        Create 30 Schedules seeds
        """
        fake = Faker()
        users = BaseModel.as_list(db.session.query(User).all())
        events = BaseModel.as_list(db.session.query(Event).all())
        stages = BaseModel.as_list(db.session.query(Stage).all())
        for i in range(0, 30):
            user_id = random.choice(users)['id']
            event_id = random.choice(events)['id']
            stage_id = random.choice(stages)['id']
            time_start = fake.future_datetime()
            rand_int = random.randint(5, 50)
            time_end = time_start + timedelta(hours=rand_int)
            schedule = {
                'user_id': user_id,
                'event_id': event_id,
                'stage_id': stage_id,
                'time_start': time_start,
                'time_end': time_end
            }
            new_schedule = Schedule()
            new_schedule.user_id = schedule['user_id']
            new_schedule.event_id = schedule['event_id']
            new_schedule.stage_id = schedule['stage_id']
            new_schedule.time_start = schedule['time_start']
            new_schedule.time_end = schedule['time_end']
            db.session.add(new_schedule)
            db.session.commit()
