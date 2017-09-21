from app.models.speaker_candidate import SpeakerCandidate
from app.models import db
from faker import Faker

'''
Seeder class for
'''


class SpeakerCandidateSeeder():

    @staticmethod
    def run():
        """
        create 10 speaker_candidates
        """
        for i in range(0, 10):
            faker = Faker()
            candidate = SpeakerCandidate()
            candidate.first_name = faker.first_name()
            candidate.last_name = faker.last_name()
            candidate.email = faker.email()
            candidate.job = faker.word()
            candidate.summary = faker.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            candidate.stage = faker.random_element(elements=('prospect', 'lead'))
            db.session.add(candidate)

        db.session.commit()
