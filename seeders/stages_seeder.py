from app.models.stage import Stage
from app.models import db

'''
Seeder class for
'''


class StagesSeeder():

    @staticmethod
    def run():
        """
        Create 3 stages seed
        """
        main_stage = Stage()
        main_stage.name = 'Main speaker stage A'
        main_stage.stage_type = 'mainstage'
        main_stage.information = 'Main Stage on left of corner of hall, will be prepared for main speakers'
        db.session.add(main_stage)
        
        podium_stage = Stage()
        podium_stage.name = 'podium stage A'
        podium_stage.stage_type = 'podium'
        podium_stage.information = 'podium stage for speakers'
        db.session.add(podium_stage)

        booth_stage = Stage()
        booth_stage.name = 'booth stage A'
        booth_stage.stage_type = 'booth'
        booth_stage.information = 'booth stage for booths'
        db.session.add(booth_stage)

        db.session.commit()
