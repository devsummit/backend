from faker import Faker
from app.models.newsletter import Newsletter
from app.models import db

'''
Seeder class for
'''


class NewsletterSeeder():

    @staticmethod
    def run():
        """
        Create 10 Newsletter seeds
        """
        fake = Faker()
        for i in range(0, 10):
            new_subscriber = Newsletter()
            new_subscriber.email = fake.safe_email()
            db.session.add(new_subscriber)
            db.session.commit()
