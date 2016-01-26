import weakref
import KBEngine

from ITEM_INFO import TItemInfo

class InventoryMgr:
	"""docstring for InventoryMgr"""
	#NOITEM = -1
	def __init__(self, entity):
		self._entity = weakref.proxy(entity)
		#self._curItemIndex = NOITEM
		#初始化背包索引index to Uid
		self.invIndex2Uids = [-1]*12
		for key, info in self._entity.itemList.items():
			self.invIndex2Uids[info[3]] = key

		#初始化装备索引index to Uid
		self.equipIndex2Uids = [-1]*4
		for key, info in self._entity.equipItemList.items():
			self.equipIndex2Uids[info[3]] = key

	def addItem(self, itemId, itemUUID = None):
		if itemUUID is None:
			itemUUID = KBEngine.genUUID64()

		emptyIndex = -1
		for i in range(0,12):
			if self.invIndex2Uids[i] == -1:
				emptyIndex = i
				break

		#背包已经满了
		if emptyIndex == -1:
			return -1

		iteminfo = TItemInfo()
		iteminfo.extend([itemUUID, itemId, 1, emptyIndex])
		self.invIndex2Uids[emptyIndex] = itemUUID

		self._entity.itemList[itemUUID] = iteminfo
		return itemUUID

	def removeItem(self, itemUUID):
		itemId = self._entity.itemList[itemUUID][1]
		itemIndex = self._entity.itemList[itemUUID][3]
		self.invIndex2Uids[itemIndex] = -1
		del self._entity.itemList[itemUUID]
		return itemId
	
	def swapItem(self, srcIndex, dstIndex):
		srcUid = self.invIndex2Uids[srcIndex]
		dstUid = self.invIndex2Uids[dstIndex]
		self.invIndex2Uids[srcIndex] = dstUid
		if dstUid != -1:
			self._entity.itemList[dstUid][3] = srcIndex
		self.invIndex2Uids[dstIndex] = srcUid
		if srcUid != -1:
			self._entity.itemList[srcUid][3] = dstIndex

		#装备或脱下
	def equipItem(self, itemIndex, equipIndex):
		invUid = self.invIndex2Uids[itemIndex]
		equipUid = self.equipIndex2Uids[equipIndex]
		#背包索引位置没有物品
		if invUid == -1 and equipUid == -1:
			return -1
		
		equipItem = {}
		if equipUid != -1:
			equipItem = self._entity.equipItemList[equipUid]
			del self._entity.equipItemList[equipUid]
			self.equipIndex2Uids[equipIndex] = -1

		if invUid != -1:
			self._entity.equipItemList[invUid] = self._entity.itemList[invUid]
			self._entity.equipItemList[invUid][3] = equipIndex
			self.equipIndex2Uids[equipIndex] = invUid
			del self._entity.itemList[invUid]
			self.invIndex2Uids[itemIndex] = -1

		if equipUid != -1:
			self._entity.itemList[equipUid] = equipItem
			self._entity.itemList[equipUid][3] = itemIndex
			self.invIndex2Uids[itemIndex] = equipUid

		



		