# -*- coding: utf-8 -*-
import random
import math
import time
import SCDefine
import d_spaces
import KBEngine
from KBEDebug import *
from interfaces.GameObject import GameObject

class DroppedItem(KBEngine.Entity, GameObject):
	"""
	这是一个掉地物品实体，可以拾取
	"""
	
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self) 
		self.pickerID = 0
		self.DESTROY_TIMER = 1001
		
	def pickUpRequest(self, whomID):
		DEBUG_MSG("DroppedItem::pickUpRequest: %i, whomID=%i." % (self.id, whomID))

		if self.pickerID == 0:
			picker = KBEngine.entities[whomID]
			picker.base.pickUpResponse(True, self.id, self.itemId, self.itemCount)
			self.pickerID = whomID
			self.addTimer(0.1,0,self.DESTROY_TIMER)

	def onTimer( self, timerId, userId):
		if userId == self.DESTROY_TIMER:
			self.destroy()