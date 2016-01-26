# -*- coding: utf-8 -*-
import KBEngine
import time
from KBEDebug import *
from interfaces.GameObject import GameObject
from interfaces.Teleport import Teleport
from Inventory import InventoryMgr

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
		self.inventory = InventoryMgr(self)

	def onEntitiesEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("Avatar[%i-%s] entities enable. spaceUTypeB=%s, mailbox:%s" % (self.id, self.nameB, self.spaceUTypeB, self.client))
		Teleport.onEntitiesEnabled(self)

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
				self.accountEntity.activeAvatar = None
				self.accountEntity.destroy()
				self.accountEntity = None
			else:
				DEBUG_MSG("Avatar[%i].destroySelf: relogin =%i" % (self.id, time.time() - self.accountEntity.relogin))
				
		# 销毁base
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

	def pickUpResponse(self, success, droppedItemID, itemID):
		if success:
			itemUUId = self.inventory.addItem(itemID)
			self.client.pickUpResponse(True, itemID, itemUUId, self.itemList[itemUUId][3])

	def dropRequest( self, itemUUId ):

		itemId = self.inventory.removeItem( itemUUId )
		self.cell.dropNotify( itemId )

	def swapItemRequest( self, srcIndex, dstIndex):
		self.inventory.swapItem(srcIndex, dstIndex)

	def equipItemRequest( self, itemIndex, equipIndex):
		if self.inventory.equipItem(itemIndex, equipIndex) == -1:
			self.client.errorInfo(4)