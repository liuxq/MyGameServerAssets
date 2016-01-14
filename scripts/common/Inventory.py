import weakref
import KBEngine

from ITEM_INFO import TItemInfo

class InventoryMgr:
	"""docstring for InventoryMgr"""
	#NOITEM = -1
	def __init__(self, entity):
		self._entity = weakref.proxy(entity)
		#self._curItemIndex = NOITEM

	def addItem(self, itemId, itemUUID = None):
		if itemUUID is None:
			itemUUID = KBEngine.genUUID64()
		iteminfo = TItemInfo()
		iteminfo.extend([itemUUID, itemId, 1])
		self._entity.itemList[itemUUID] = iteminfo
		return itemUUID

	def removeItem(self, itemUUID):
		itemId = self._entity.itemList[itemUUID][1]
		del self._entity.itemList[itemUUID]
		return itemId
			




		