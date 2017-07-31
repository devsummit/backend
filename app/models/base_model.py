class BaseModel:
	''' Base of all model class contains helper method to simplify jobs '''

	'''
	method to return model class as dict
	'''
	def as_dict(self):
		''' return readable field if set, and all field otherwise '''
		if hasattr(self, 'readable'):
			return {c: getattr(self, c) for c in self.visible}
		else:
			return {c.name: getattr(self, c.name) for c in self.__table__.columns}
