from app.controllers.base_controller import BaseController
from app.services import hackteamservice
from app.services import orderservice


class HackTeamController(BaseController):
    @staticmethod
    def index():
        teams = hackteamservice.get()
        return BaseController.send_response_api(teams['data'], teams['message'])

    @staticmethod
    def show(id):
        team = hackteamservice.show(id)
        if team['error']:
            return BaseController.send_error_api(team['data'], team['message'])
        return BaseController.send_response_api(team['data'], team['message'])

    @staticmethod
    def delete(request, id):
        order_id = request.json['order_id'] if 'order_id' in request.json else None
        if order_id is None:
            return BaseController.send_error_api(None, 'invalid payload')
        result = hackteamservice.delete(id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        # delete order too
        orderservice.delete(order_id)
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def create(request, user_id):
        team = request.json['team'] if 'team' in request.json else None
        order = request.json['order'] if 'order' in request.json else None

        if team is None or order is None:
            return BaseController.send_error_api(None, 'field is not complete')
        if 'order_details' not in order:
            return BaseController.send_error_api(None, 'field is not complete')

        referal_code = order['referal_code'] if 'referal_code' in order else None
        team_name = team['team_name'] if 'team_name' in team else None
        project_name = team['project_name'] if 'project_name' in team else ''

        if order['order_details'] is None or len(order['order_details']) < 1:
            return BaseController.send_error_api({'payload_invalid': True}, 'payload is invalid')

        if project_name and order:
            team_payload = {
                'team_name': team_name,
                'project_name': project_name,
                'user_id': user_id                
            }

            order_payload = {
                'user_id': user_id,
                'order_details': order['order_details'],
                'referal_code': referal_code 
            }

        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = hackteamservice.create(team_payload, user_id)

        if not result['error']:
            # orders
            order_result = orderservice.create(order_payload)
            return BaseController.send_response_api(result['data'], result['message'], order_result['data'])
        else:
            return BaseController.send_error_api(result['data'], result['message'])
