import datetime


class BaseModel:
	''' Base of all model class contains helper method to simplify jobs '''

	'''
	method to return model class as dict
	'''

	def as_dict(self):
		''' return readable field if set, and all field otherwise '''
		if hasattr(self, 'visible'):
			result = {}
			for c in self.visible:
				if c in ['created_at', 'updated_at', 'time_start', 'time_end']:
					result[c] = datetime.datetime.strftime(getattr(self, c), '%Y-%m-%d %H:%M:%S') if getattr(self, c) else None
					continue
				result[c] = getattr(self, c)
			return result
		else:
			for c in self.__table__.columns:
				if c in ['created_at', 'updated_at', 'time_start', 'time_end']:
					result[c] = datetime.datetime.strftime(getattr(self, c), '%Y-%m-%d %H:%M:%S') if getattr(self, c) else None
					continue
				result[c] = getattr(self, c)
			return result

	'''
	method to return list of query resutl as array dict
	'''
	@staticmethod
	def as_list(result):
		result_list = []
		for res in result:
			result_list.append(res.as_dict())
		return result_list
