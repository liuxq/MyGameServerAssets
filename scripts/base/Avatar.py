# -*- coding: utf-8 -*-
import KBEngine
import time

from KBEDebug import *
from interfaces.GameObject import GameObject
from interfaces.Teleport import Teleport
from Inventory import InventoryMgr

from ITEM_INFO import TItemInfo

import items

class Avatar(KBEngine.Proxy,
			GameObject,
			Teleport):
	"""
	角色实体
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		GameObject.__init__(self)
		Teleport.__init__(self)
		
		self.accountEntity = None
		self.cellData["dbid"] = self.databaseID
		self.nameB = self.cellData["name"]
		self.spaceUTypeB = self.cellData["spaceUType"]
		
		self._destroyTimer = 0
		self.inventory = InventoryMgr(self)

	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("Avatar[%i-%s] entities enable. spaceUTypeB=%s, entityCall:%s" % (self.id, self.nameB, self.spaceUTypeB, self.client))
		Teleport.onClientEnabled(self)
		
		if self._destroyTimer > 0:
			self.delTimer(self._destroyTimer)
			self._destroyTimer = 0

	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG('Avatar::onGetCell: %s' % self.cell)
		
	def createCell(self, space):
		"""
		defined method.
		创建cell实体
		"""
		self.createCellEntity(space)
	
	def destroySelf(self):
		"""
		"""
		if self.client is not None:
			return
			
		if self.cell is not None:
			# 销毁cell实体
			self.destroyCellEntity()
			return
			
		# 如果帐号ENTITY存在 则也通知销毁它
		if self.accountEntity != None:
			if time.time() - self.accountEntity.relogin > 1:
				self.accountEntity.destroy()
			else:
				DEBUG_MSG("Avatar[%i].destroySelf: relogin =%i" % (self.id, time.time() - self.accountEntity.relogin))
				
		# 销毁base
		if not self.isDestroyed:
			self.destroy()

	def onClientDeath(self):
		"""
		KBEngine method.
		entity丢失了客户端实体
		"""
		DEBUG_MSG("Avatar[%i].onClientDeath:" % self.id)
		self.destroySelf()

	def sendChatMessage(self, msg):
		DEBUG_MSG("Avatar[%i].sendChatMessage:" % self.id)
		for player in KBEngine.entities.values():
			if player.__class__.__name__ == "Avatar":
				player.client.ReceiveChatMessage(msg)

	def reqItemList(self):
		if self.client:
			self.client.onReqItemList(self.itemList, self.equipItemList)

	def pickUpResponse(self, success, droppedItemID, itemID, itemCount):
		if success:
			itemUUIdList = self.inventory.addItem(itemID,itemCount)
			for uuid in itemUUIdList:
				self.client.pickUp_re(self.itemList[uuid])

	def dropRequest( self, itemUUId ):
		itemCount = self.itemList[itemUUId][2]
		itemId = self.inventory.removeItem( itemUUId, itemCount)
		self.cell.dropNotify( itemId, itemUUId , itemCount)

	def swapItemRequest( self, srcIndex, dstIndex):
		self.inventory.swapItem(srcIndex, dstIndex)

	def equipItemRequest( self, itemIndex, equipIndex):
		if self.inventory.equipItem(itemIndex, equipIndex) == -1:
			self.client.errorInfo(4)
		else:
			#传回去装备和物品信息
			itemUUId = self.inventory.getItemUidByIndex(itemIndex)
			equipUUId = self.inventory.getEquipUidByIndex(equipIndex)
			itemInfo = TItemInfo()
			itemInfo.extend([0, 0, 0, itemIndex])
			equipItemInfo = TItemInfo()
			equipItemInfo.extend([0, 0, 0, equipIndex])
			if itemUUId != 0:
				itemInfo = self.itemList[itemUUId]
			if equipUUId != 0:
				equipItemInfo = self.equipItemList[equipUUId]
			self.client.equipItemRequest_re(itemInfo,equipItemInfo)
			#--------------------
			avatarCell = self.cell
			avatarCell.resetPropertys()
			for key, info in self.equipItemList.items():
				items.getItem(info[1]).use(self)

			if equipIndex == 0:
				uid = self.inventory.getEquipUidByIndex(equipIndex)
				if uid == 0:
					avatarCell.equipNotify(-1)
				else:
					avatarCell.equipNotify(self.equipItemList[uid][1])

	def updatePropertys(self):
		avatarCell = self.cell
		avatarCell.resetPropertys()
		for key, info in self.equipItemList.items():
			items.getItem(info[1]).use(self)
			
				
	def useItemRequest(self, itemIndex):
		itemUUId = self.inventory.getItemUidByIndex(itemIndex)
		item = items.getItem(self.itemList[itemUUId][1])
		item.use(self)
		itemCount = self.itemList[itemUUId][2]
		itemId = self.inventory.removeItem( itemUUId, 1 )
		if itemId == -1:#只是减少物品数量，并没有销毁
			self.client.pickUp_re(self.itemList[itemUUId])
		else:#销毁物品
			self.client.dropItem_re( itemId, itemUUId)
			
	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		
		if self.accountEntity != None:
			self.accountEntity.activeAvatar = None
			self.accountEntity = None



