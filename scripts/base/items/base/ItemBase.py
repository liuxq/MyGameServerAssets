

class ItemBase:
	"""物品基类"""
	def __init__(self):
		NONE_TYPE = -1
		STAFF_TYPE = 2

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		从字典中创建这个对象
		"""
		self._id = dictDatas.get('id', 0)
	
	def getID(self):
		return self._id
