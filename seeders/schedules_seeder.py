from datetime import timedelta, datetime
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
        count = 0
        while count < 5:
            new_schedule = Schedule()
            new_schedule.event_id = 1
            new_schedule.stage_id = 1
            new_schedule.time_start = datetime.strptime("2017-11-21 13:33:54", '%Y-%m-%d %H:%M:%S')
            new_schedule.time_end = new_schedule.time_start + timedelta(hours=1)
            db.session.add(new_schedule)
            db.session.commit()
            count += 1

        count = 0
        while count < 5:
            new_schedule = Schedule()
            new_schedule.event_id = 1
            new_schedule.stage_id = 1
            new_schedule.time_start = datetime.strptime("2017-11-22 13:33:54", '%Y-%m-%d %H:%M:%S')
            new_schedule.time_end = new_schedule.time_start + timedelta(hours=1)
            db.session.add(new_schedule)
            db.session.commit()
            count += 1

        count = 0
        while count < 5:
            new_schedule = Schedule()
            new_schedule.event_id = 1
            new_schedule.stage_id = 1
            new_schedule.time_start = datetime.strptime("2017-11-23 13:33:54", '%Y-%m-%d %H:%M:%S')
            new_schedule.time_end = new_schedule.time_start + timedelta(hours=1)
            db.session.add(new_schedule)
            db.session.commit()
            count += 1
