# -*- coding: utf-8 -*-
import KBEngine
import GlobalDefine
from KBEDebug import *
from interfaces.GameObject import GameObject
from interfaces.Motion import Motion
from interfaces.Teleport import Teleport

class Avatar(KBEngine.Entity,
				GameObject,
				Motion,
				Teleport):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		Motion.__init__(self)
		Teleport.__init__(self) 

		# 设置每秒允许的最快速度, 超速会被拉回去
		self.topSpeed = self.moveSpeed + 5.0
		# self.topSpeedY = 10.0

	def isPlayer(self):
		"""
		virtual method.
		"""
		return True

	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		Teleport.onDestroy(self)
		
	