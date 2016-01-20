import weakref
import KBEngine

from ITEM_INFO import TItemInfo

class InventoryMgr:
	"""docstring for InventoryMgr"""
	#NOITEM = -1
	def __init__(self, entity):
		self._entity = weakref.proxy(entity)
		#self._curItemIndex = NOITEM
		self.index2Uids = [-1]*12
		for key, info in self._entity.itemList.items():
			self.index2Uids[info[3]] = key

	def addItem(self, itemId, itemUUID = None):
		if itemUUID is None:
			itemUUID = KBEngine.genUUID64()

		emptyIndex = -1
		for i in range(0,12):
			if self.index2Uids[i] == -1:
				emptyIndex = i
				break

		#背包已经满了
		if emptyIndex == -1:
			return -1

		iteminfo = TItemInfo()
		iteminfo.extend([itemUUID, itemId, 1, emptyIndex])
		self.index2Uids[emptyIndex] = itemUUID

		self._entity.itemList[itemUUID] = iteminfo
		return itemUUID

	def removeItem(self, itemUUID):
		itemId = self._entity.itemList[itemUUID][1]
		itemIndex = self._entity.itemList[itemUUID][3]
		self.index2Uids[itemIndex] = -1
		del self._entity.itemList[itemUUID]
		return itemId
	
	def swapItem(self, srcIndex, dstIndex):
		srcUid = self.index2Uids[srcIndex]
		dstUid = self.index2Uids[dstIndex]
		self.index2Uids[srcIndex] = dstUid
		if dstUid != -1:
			self._entity.itemList[dstUid][3] = srcIndex
		self.index2Uids[dstIndex] = srcUid
		if srcUid != -1:
			self._entity.itemList[srcUid][3] = dstIndex




		