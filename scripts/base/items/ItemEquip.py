# -*- coding: utf-8 -*-
import KBEngine
import GlobalConst
from KBEDebug import * 
from items.base.ItemBase import ItemBase

class ItemEquip(ItemBase):
	def __init__(self):
		ItemBase.__init__(self)

	def loadFromDict(self, dictDatas):
		"""
		virtual method.
		从字典中创建这个对象
		"""
		ItemBase.loadFromDict(self, dictDatas)
		
		self.defence = dictDatas.get('defence', 0)
		self.attack_Max = dictDatas.get("attack_Max", 0)
		self.attack_Min = dictDatas.get("attack_Min", 0)

	def canUse(self, user):
		return GlobalConst.GC_OK
		
	def use(self, user):
		if self.defence > 0:
			user.cell.addDefence(self.defence)
		if self.attack_Max > 0:
			user.cell.addAttack_Max(self.attack_Max)
		if self.attack_Min > 0:
			user.cell.addAttack_Min(self.attack_Min)
			
		return GlobalConst.GC_OK