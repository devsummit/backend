class BaseService():

    def __init__(self, page=0, base_url='', total_items=0):
        self.page = page
        self.base_url = base_url
        self.total_items = total_items

    def paginate(self, query):
        results = query.paginate(int(self.page), int(self.perpage), False)
        self.paginated = {}
        links = {}

        links['prev'] = (self.base_url + '?page=' + str(results.prev_num)) if results.prev_num else None
        links['next'] = (self.base_url + '?page=' + str(results.next_num)) if results.next_num else None
        links['curr'] = self.base_url + '?page=' + str(self.page)
        links['total_items'] = self.total_items

        self.paginated['data'] = results.items
        self.paginated['links'] = links

        return self.paginated

    def include(self, fields):
        _results = []
        for item in self.paginated['data']:
            data = item.as_dict()
            for field in fields:
                data[field] = getattr(item, field).as_dict() if getattr(item, field) else None
            _results.append(data)
        self.paginated['data'] = _results
        return self.paginated

    def transform(self):
        _results = []
        for item in self.paginated['data']:
            item = item.as_dict()
            _results.append(item)
        self.paginated['data'] = _results
        return self.paginated
