from app.models.client import Client
from app.models import db
import datetime

'''
Seeder class for
'''


class ClientsSeeder():
    @staticmethod
    def run():
        """
        Create clients seeder
        """
        data = [
            {
                'app_name': "password_grant",
                'client_secret': "sup3rs3cr3t",
                'client_id': "sup3rs3cr3t"
            },
            {
                'app_name': "google",
                'client_secret': "ZdbNXvmMTy9dcAK8oW-3QPOj",
                'client_id': "1091376735288-sgpfaq0suha3qakagrsig7bee58enkqr.apps.googleusercontent.com"
            },
            {
                'app_name': "facebook",
                'client_secret': "0463ed52bd8a400dd48d8e9cc246acc4",
                'client_id': "216608565531165"
            },
            {
                'app_name': "twitter",
                'client_secret': "eJBRnVvE0YplptEelYJOuHYw2YLdOf9v39YNnfdM6Rkv3kNShC",
                'client_id': "iJoptl48l8j5OseOI1lrS3r9N"
            },
        ]

        for _data in data:
            new_client = Client()
            new_client.app_name = _data['app_name']
            new_client.client_secret = _data['client_secret']
            new_client.client_id = _data['client_id']
            new_client.created_at = datetime.datetime.now()
            new_client.updated_at = datetime.datetime.now()
            db.session.add(new_client)
            db.session.commit()
