import eventbrite
import logging
from app.models import db
# import model class
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from app.configs.constants import EVENT_BRITE
from app.builders.response_builder import ResponseBuilder


class EventBriteService(BaseService):

    def __init__(self): 
        self.event_id = EVENT_BRITE['EVENTBRITE_EVENT_ID']
        self.eventbrite = eventbrite.Eventbrite(EVENT_BRITE['EVENTBRITE_OAUTH_TOKEN'])

    def hook(self, request):
        response = ResponseBuilder()
        hook_object = self.eventbrite.webhook_to_object(request)
        logging.info(hook_object)
        logging.debug(hook_object)

        if hook_object.type == 'Order':
            # do something to order hook
            pass

    # testing the sdk
    def events(self, request):
        response = ResponseBuilder()
        events = self.eventbrite.get_event(self.event_id)
        result = {
            'name': events['name']['text'],
            'description': events['description']['text'],
            'id': events['id'],
            'url': events['url'],
            'start': events['start'],
            'end': events['end']
        }

        return response.set_data(result).set_message('Event retrieved from eventbrite').build()
