from faker import Faker
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
            new_beacon = Beacon()
            new_beacon.code = fake.pystr(min_chars=8, max_chars=8)
            db.session.add(new_beacon)
            db.session.commit()
