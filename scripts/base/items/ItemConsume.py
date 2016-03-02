# -*- coding: utf-8 -*-
import KBEngine
import random
import GlobalConst
from KBEDebug import * 
from items.base.ItemBase import ItemBase

class ItemConsume(ItemBase):
	def __init__(self):
		ItemBase.__init__(self)

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		从字典中创建这个对象
		"""
		ItemBase.loadFromDict(self, dictDatas)
		
		# 加血
		self.hp = dictDatas.get('hp', 0)
		
		# 加魔法
		self.mp = dictDatas.get("mp", 0)
		
		# cd
		self.limitCD = dictDatas.get("limitCD", 1)
		
	def getHp(self):
		return self.hp

	def getMp(self):
		return self.mp

	def canUse(self, user):
		return GlobalConst.GC_OK
		
	def use(self, user):
		if self.hp > 0:
			user.cell.addHP(self.hp)
		if self.mp > 0:
			user.cell.addMP(self.mp)

		return GlobalConst.GC_OK