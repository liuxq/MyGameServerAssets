# -*- coding: utf-8 -*-
import KBEngine
import KBExtra
import random, math
import Math
from KBEDebug import *
from interfaces.GameObject import GameObject
from interfaces.Dialog import Dialog
from interfaces.Teleport import Teleport
from interfaces.State import State
from interfaces.Flags import Flags
from interfaces.Combat import Combat
from interfaces.Spell import Spell
from interfaces.SkillBox import SkillBox
from interfaces.Motion import Motion

class Avatar(KBEngine.Entity,
			GameObject,
			Flags,
			State,
			SkillBox,
			Combat, 
			Spell, 
			Dialog,
			Motion,
			Teleport):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		Flags.__init__(self) 
		State.__init__(self) 
		SkillBox.__init__(self) 
		Combat.__init__(self) 
		Spell.__init__(self) 
		Dialog.__init__(self)
		Motion.__init__(self)
		Teleport.__init__(self)
		
	def onEnterSpace(self):
		"""
		KBEngine method.
		这个entity进入了一个新的space
		"""
		DEBUG_MSG("%s::onEnterSpace: %i" % (self.__class__.__name__, self.id))

	def onLeaveSpace(self):
		"""
		KBEngine method.
		这个entity将要离开当前space
		"""
		DEBUG_MSG("%s::onLeaveSpace: %i" % (self.__class__.__name__, self.id))
		
	def onBecomePlayer( self ):
		"""
		KBEngine method.
		当这个entity被引擎定义为角色时被调用
		"""
		DEBUG_MSG("%s::onBecomePlayer: %i" % (self.__class__.__name__, self.id))
		
	def onJump(self):
		"""
		defined method.
		玩家跳跃
		"""
		pass
#####测试用，不实现##################################
	def ReceiveChatMessage(self, str):
		DEBUG_MSG("ReceiveChatMessage:%s" % (str))

	def onReqItemList(itemList, equipList):
		pass

	def pickUp_re(item_info):
		pass
	def dropItem_re(itemId, dbid):
		pass
	def equipItemRequest_re(item_info, item_info2):
		pass
	def errorInfo(errorCode):
		pass
		
class PlayerAvatar(Avatar):
	def __init__(self):
		self.randomWalkRadius = 10.0
		
	def onEnterSpace(self):
		"""
		KBEngine method.
		这个entity进入了一个新的space
		"""
		DEBUG_MSG("%s::onEnterSpace: %i" % (self.__class__.__name__, self.id))
		
		# 注意：由于PlayerAvatar是引擎底层强制由Avatar转换过来，__init__并不会再调用
		# 这里手动进行初始化一下
		self.__init__()
		
		self.spawnPosition = Math.Vector3( self.position )
		KBEngine.callback(1, self.updateMove)
		
	def onLeaveSpace(self):
		"""
		KBEngine method.
		这个entity将要离开当前space
		"""
		DEBUG_MSG("%s::onLeaveSpace: %i" % (self.__class__.__name__, self.id))

	def calcRandomWalkPosition( self ):
		"""
		计算随机移动位置
		"""
		center = self.spawnPosition
		r = random.uniform( 1, self.randomWalkRadius ) # 最少走1米
		b = 360.0 * random.random()
		x = r * math.cos( b )		# 半径 * 正余玄
		z = r * math.sin( b )
		return Math.Vector3( center.x + x, center.y, center.z + z )

	def updateMove(self):
		#DEBUG_MSG("%s::updateMove: %i" % (self.__class__.__name__, self.id))
		KBEngine.callback(1, self.updateMove)
		self.moveToPoint( self.calcRandomWalkPosition(), self.velocity, 0.0, 0, True, True )



