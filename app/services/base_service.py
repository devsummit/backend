from app.models.base_model import BaseModel


class BaseService():

    def __init__(self, page=0, base_url='', total_items=0):
        self.page = page
        self.base_url = base_url
        self.total_items = total_items

    def paginate(self, query):
        results = query.paginate(int(self.page), int(self.perpage), False)
        paginate = {}
        links = {}

        links['prev'] = (self.base_url + '?page=' + str(results.prev_num)) if results.prev_num else None
        links['next'] = (self.base_url + '?page=' + str(results.next_num)) if results.next_num else None
        links['curr'] = self.base_url + '?page=' + str(self.page)
        links['total_items'] = self.total_items

        paginate['data'] = BaseModel.as_list(results.items)
        paginate['links'] = links

        return paginate
