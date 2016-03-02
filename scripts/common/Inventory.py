import weakref
import KBEngine
from KBEDebug import *

import d_items
from ITEM_INFO import TItemInfo


class InventoryMgr:
	"""docstring for InventoryMgr"""
	#NOITEM = -1
	def __init__(self, entity):
		self._entity = weakref.proxy(entity)
		#self._curItemIndex = NOITEM
		#初始化背包索引index to Uid
		self.invIndex2Uids = [0]*12
		for key, info in self._entity.itemList.items():
			self.invIndex2Uids[info[3]] = key

		#初始化装备索引index to Uid
		self.equipIndex2Uids = [0]*4
		for key, info in self._entity.equipItemList.items():
			self.equipIndex2Uids[info[3]] = key

	def addItem(self, itemId, itemCount = 1):
		result = []
		emptyIndex = -1
		for i in range(0,12):
			if self.invIndex2Uids[i] == 0:
				emptyIndex = i
				break
		#背包已经满了
		if emptyIndex == -1:
			return result
		#放置物品
		itemStack = d_items.datas[itemId]['itemStack']
		
		#不可堆叠物品
		if itemStack == 1:
			itemUUID = KBEngine.genUUID64()
			iteminfo = TItemInfo()
			iteminfo.extend([itemUUID, itemId, 1, emptyIndex])
			self.invIndex2Uids[emptyIndex] = itemUUID
			self._entity.itemList[itemUUID] = iteminfo
			result.append(itemUUID)
			
		#可堆叠物品
		else:
			for key, info in self._entity.itemList.items():
				if info[1] == itemId and info[2] < itemStack:
					info[2] += itemCount
					result.append(key)
					if info[2] > itemStack:
						itemCount = info[2]-itemStack
						info[2] = itemStack
					else:
						itemCount = 0
						break

			if itemCount > 0:
				itemUUID = KBEngine.genUUID64()
				iteminfo = TItemInfo()
				iteminfo.extend([itemUUID, itemId, itemCount, emptyIndex])
				self.invIndex2Uids[emptyIndex] = itemUUID
				self._entity.itemList[itemUUID] = iteminfo
				result.append(itemUUID)

		return result
		

	def removeItem(self, itemUUID, itemCount):
		itemId = self._entity.itemList[itemUUID][1]
		itemC = self._entity.itemList[itemUUID][2]
		itemIndex = self._entity.itemList[itemUUID][3]
		if itemCount < itemC:
			self._entity.itemList[itemUUID][2] = itemC - itemCount
			return -1
		else:
			self.invIndex2Uids[itemIndex] = 0
			del self._entity.itemList[itemUUID]
		return itemId
	
	def swapItem(self, srcIndex, dstIndex):
		srcUid = self.invIndex2Uids[srcIndex]
		dstUid = self.invIndex2Uids[dstIndex]
		self.invIndex2Uids[srcIndex] = dstUid
		if dstUid != 0:
			self._entity.itemList[dstUid][3] = srcIndex
		self.invIndex2Uids[dstIndex] = srcUid
		if srcUid != 0:
			self._entity.itemList[srcUid][3] = dstIndex

		#装备或脱下
	def equipItem(self, itemIndex, equipIndex):
		invUid = self.invIndex2Uids[itemIndex]
		equipUid = self.equipIndex2Uids[equipIndex]
		#背包索引位置没有物品
		if invUid == 0 and equipUid == 0:
			return -1
		
		equipItem = {}
		if equipUid != 0:
			equipItem = self._entity.equipItemList[equipUid]
			del self._entity.equipItemList[equipUid]
			self.equipIndex2Uids[equipIndex] = 0

		if invUid != 0:
			self._entity.equipItemList[invUid] = self._entity.itemList[invUid]
			self._entity.equipItemList[invUid][3] = equipIndex
			self.equipIndex2Uids[equipIndex] = invUid
			del self._entity.itemList[invUid]
			self.invIndex2Uids[itemIndex] = 0

		if equipUid != 0:
			self._entity.itemList[equipUid] = equipItem
			self._entity.itemList[equipUid][3] = itemIndex
			self.invIndex2Uids[itemIndex] = equipUid

	def getItemUidByIndex(self, itemIndex):
		return self.invIndex2Uids[itemIndex]
	def getEquipUidByIndex(self, equipIndex):
		return self.equipIndex2Uids[equipIndex]

		



		