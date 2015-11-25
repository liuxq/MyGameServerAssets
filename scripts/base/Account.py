# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onEntitiesEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. mailbox:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()
	def reqHello(self):
		DEBUG_MSG("Account[%i].reqHello:" % self.id)
		self.client.onHello("刘晓强")

	def reqCreateAvatar(self, name, roleType):
		props = {
					"level": 1,
					"name": name,
					"roleType": roleType
		}
		avatar = KBEngine.createBaseLocally("Avatar",props)
		if avatar:
			avatar.writeToDB(self._onCharacterSaved)
		

	def _onCharacterSaved(self, success, avatar):
		if success:
			info = {
				"dbid": avatar.databaseID,
				"name": avatar.cellData["name"],
				"roleType": avatar.roleType,
				"level": 1
			}

			self.characters["value"].extend([info])
			self.writeToDB()
			avatar.destroy()

			if self.client:
				self.client.onCreateAvatarResult(0, info)