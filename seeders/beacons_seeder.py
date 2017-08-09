from faker import Faker
from datetime import timedelta
from app.models.beacon import Beacon
from app.models import db

'''
Seeder class for
'''


class BeaconsSeeder():

    @staticmethod
    def run():
        """
        Create 20 Beacons seeds
        """
        fake = Faker()
        for i in range(0, 20):
            code = fake.pystr(min_chars=8, max_chars=8)
            beacon = {
                'code': code
            }
            
            new_beacon = Beacon()
            new_beacon.code = beacon['code']
            db.session.add(new_beacon)
            db.session.commit()
