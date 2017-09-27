from app.controllers.base_controller import BaseController
from app.services import feedreportservice


class FeedReportController(BaseController):

    @staticmethod
    def index(request, page=None):
        feed_reports = feedreportservice.get(request, page=page)
        return BaseController.send_response_api(feed_reports['data'], feed_reports['message'], {}, feed_reports['links'])

    @staticmethod
    def create(request, user_id):
        feed_reports = feedreportservice.get(request, page=None)
        report_type = request.json['report_type'] if 'report_type' in request.json else None
        feed_id = request.json['feed_id'] if 'feed_id' in request.json else None
        if user_id and report_type and feed_id:
            payloads = {
                'user_id': user_id,
                'report_type': report_type,
                'feed_id': feed_id
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')
        
        for feed_report in feed_reports['data']:
            if user_id == feed_report['user_id'] and feed_id == feed_report['feed_id']:
                return BaseController.send_error_api(None, 'You already report this feed')
                break
            else:
                result = feedreportservice.create(payloads)
                break
        else:
            result = feedreportservice.create(payloads)            

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def show(id):
        feed = feedreportservice.show(id)
        if feed['error']:
            return BaseController.send_error_api(feed['data'], feed['message'])
        return BaseController.send_response_api(feed['data'], feed['message'])
