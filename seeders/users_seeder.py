from app.models.user import User
from app.models.attendee import Attendee
from app.models.booth import Booth
from app.models.speaker import Speaker
from app.models import db

'''
Seeder class for
'''


class UsersSeeder():

    @staticmethod
    def run():
        """
        Create 4 Users seeds
        """
        # create admin
        admin = User()
        admin.first_name = 'Admin'
        admin.last_name = 'Herman'
        admin.email = 'admin@devsummit.com'
        admin.username = 'admin'
        admin.hash_password('supersecret')
        admin.role_id = 1
        db.session.add(admin)

        # create ganesh
        ganesh = User()
        ganesh.first_name = 'Ganesh'
        ganesh.last_name = 'Cauda'
        ganesh.email = 'caudaganesh@gmail.com'
        ganesh.username = 'ganesh'
        ganesh.hash_password('supersecret')
        ganesh.role_id = 7
        ganesh.points = 0
        db.session.add(ganesh)

        # create erdi
        erdi = User()
        erdi.first_name = 'Erdi'
        erdi.last_name = 'yansah'
        erdi.email = 'erdiyansah@gmail.com'
        erdi.username = 'erdi'
        erdi.hash_password('supersecret')
        erdi.role_id = 3
        db.session.add(erdi)

        # create mgufrone
        guffy = User()
        guffy.first_name = 'Mochamad'
        guffy.last_name = 'Gufrone'
        guffy.email = 'mgufrone@gmail.com'
        guffy.username = 'guffy'
        guffy.hash_password('supersecret')
        guffy.role_id = 4
        db.session.add(guffy)

        db.session.commit()

        # create booth for erdi
        erdi_booth = Booth()
        erdi_booth.user_id = 3
        erdi_booth.points = 10000
        erdi_booth.stage = None
        erdi_booth.summary = 'Promoting Mytrhil.js to Indonesia'
        db.session.add(erdi_booth)

        # create speaker for guffy
        guffy_speaker = Speaker()
        guffy_speaker.user_id = 4
        guffy_speaker.information = '-'
        guffy_speaker.summary = 'code 24.1 hours'
        guffy_speaker.job = 'COO & Senior software developer at Refactory'
        db.session.add(guffy_speaker)

        db.session.commit()
