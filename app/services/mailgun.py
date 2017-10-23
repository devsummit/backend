import requests
from app.configs.constants import MAILGUN

def gun_send_email(receiver, subject, content):
	# receiver will be formated in -> Name <email>
    return requests.post(
        MAILGUN['server'],
        auth=("api", MAILGUN['key']),
        data={"from": MAILGUN['sender'],
              "to": receiver,
              "subject": subject,
              "text": content
              }
		)