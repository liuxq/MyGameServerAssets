# -*- coding: utf-8 -*-
import KBEngine
import random
import SCDefine
import copy
import math
from KBEDebug import *
from interfaces.GameObject import GameObject
import d_entities
import d_spaces
#import d_spaces_spawns
import xml.etree.ElementTree as etree 

class Space(KBEngine.Base, GameObject):
	"""
	一个可操控cellapp上真正space的实体
	注意：它是一个实体，并不是真正的space，真正的space存在于cellapp的内存中，通过这个实体与之关联并操控space。
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)
		self.createInNewSpace(None)
		
		self.spaceUTypeB = self.cellData["spaceUType"]
		
		self.spaceResName = d_spaces.datas.get(self.spaceUTypeB)['resPath']
		
		# 这个地图上创建的entity总数
		#self.tmpCreateEntityDatas = copy.deepcopy(d_spaces_spawns.datas.get(self.spaceUTypeB, ()))
		
		self.avatars = {}
		#self.createSpawnPointDatas()
		
				
	def loginToSpace(self, avatarMailbox, context):
		"""
		defined method.
		某个玩家请求登陆到这个space中
		"""
		avatarMailbox.createCell(self.cell)
		self.onEnter(avatarMailbox)
		
	def logoutSpace(self, entityID):
		"""
		defined method.
		某个玩家请求登出这个space
		"""
		self.onLeave(entityID)
		
	def teleportSpace(self, entityMailbox, position, direction, context):
		"""
		defined method.
		请求进入某个space中
		"""
		entityMailbox.cell.onTeleportSpaceCB(self.cell, self.spaceUTypeB, position, direction)
		
	def onEnter(self, entityMailbox):
		"""
		defined method.
		进入场景
		"""
		self.avatars[entityMailbox.id] = entityMailbox
		
		if self.cell is not None:
			self.cell.onEnter(entityMailbox)
		
	def onLeave(self, entityID):
		"""
		defined method.
		离开场景
		"""
		if entityID in self.avatars:
			del self.avatars[entityID]
		
		if self.cell is not None:
			self.cell.onLeave(entityID)

	def onLoseCell(self):
		"""
		KBEngine method.
		entity的cell部分实体丢失
		"""
		KBEngine.globalData["Spaces"].onSpaceLoseCell(self.spaceUTypeB, self.spaceKey)
		GameObject.onLoseCell(self)
		
	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG("Space::onGetCell: %i" % self.id)
		self.addTimer(0.1, 0.1, SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK)
		KBEngine.globalData["Spaces"].onSpaceGetCell(self.spaceUTypeB, self, self.spaceKey)
		GameObject.onGetCell(self)
		

