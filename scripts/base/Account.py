# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import d_spaces
import d_avatar_inittab
import GlobalConst
import time

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.activeCharacter = None

		self.relogin = time.time()
		
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

	def reqAvatarList(self):
		"""
		exposed.
		客户端请求查询角色列表
		"""
		DEBUG_MSG("Account[%i].reqAvatarList: size=%i." % (self.id, len(self.characters["value"])))
		self.client.onReqAvatarList(self.characters)
	def reqCreateAvatar(self, name, roleType):

		
		if len(self.characters["value"]) >= 3:
			DEBUG_MSG("Account[%i].reqCreateAvatar:%s. character=%s.\n" % (self.id, name, self.characters))
			info = {
				"dbid": 0,
				"name": "null",
				"roleType": 1,
				"level": 1
			}
			self.client.onCreateAvatarResult(3, info)
			return
		
		""" 根据前端类别给出出生点
		UNKNOWN_CLIENT_COMPONENT_TYPE	= 0,
		CLIENT_TYPE_MOBILE				= 1,	// 手机类
		CLIENT_TYPE_PC					= 2,	// pc， 一般都是exe客户端
		CLIENT_TYPE_BROWSER				= 3,	// web应用， html5，flash
		CLIENT_TYPE_BOTS				= 4,	// bots
		CLIENT_TYPE_MINI				= 5,	// 微型客户端
		"""
		spaceUType = GlobalConst.g_demoMaps.get(self.getClientDatas(), 1)
		spaceData = d_spaces.datas.get(spaceUType)
		
		props = {
			"name"				: name,
			"roleType"			: roleType,
			"level"				: 1,
			"spaceUType"		: spaceUType,
			"direction"			: (0, 0, d_avatar_inittab.datas[roleType]["spawnYaw"]),
			"position"			: spaceData.get("spawnPos", (0,0,0))
			}
		avatar = KBEngine.createBaseLocally("Avatar",props)
		if avatar:
			avatar.writeToDB(self._onCharacterSaved)
	def reqRemoveAvatar(self, name):
		"""
		exposed.
		客户端请求删除一个角色
		"""
		DEBUG_MSG("Account[%i].reqRemoveAvatar: %s" % (self.id, name))
		found = 0
		for info in self.characters["value"]:
			if info["name"] == name:
				self.characters["value"].remove(info)
				found = info["dbid"]
				break
			
		self.client.onRemoveAvatar(found)

	def selectAvatarGame(self, dbid):
		"""
		exposed.
		客户端选择某个角色进行游戏
		"""
		DEBUG_MSG("Account[%i].selectAvatarGame:%i. self.activeCharacter=%s" % (self.id, dbid, self.activeCharacter))
		# 注意:使用giveClientTo的entity必须是当前baseapp上的entity
		if self.activeCharacter is None:
			found = 0
			for info in self.characters["value"]:
				if info["dbid"] == dbid:
					found = 1
					break
			if found == 1:
				#self.lastSelCharacter = dbid
				player = KBEngine.createBaseFromDBID("Avatar", dbid, self.__onAvatarCreated)
			else:
				ERROR_MSG("Account[%i]::selectAvatarGame: not found dbid(%i)" % (self.id, dbid))
		else:
			self.giveClientTo(self.activeCharacter)
		
	def __onAvatarCreated(self, baseRef, dbid, wasActive):
		"""
		选择角色进入游戏时被调用
		"""
		if wasActive:
			ERROR_MSG("Account::__onAvatarCreated:(%i): this character is in world now!" % (self.id))
			return
		if baseRef is None:
			ERROR_MSG("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
			return
			
		avatar = KBEngine.entities.get(baseRef.id)
		if avatar is None:
			ERROR_MSG("Account::__onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
			return
		
		if self.isDestroyed:
			ERROR_MSG("Account::__onAvatarCreated:(%i): i dead, will the destroy of Avatar!" % (self.id))
			avatar.destroy()
			return
			
		role = 1
		for info in self.characters["value"]:
			if info["dbid"] == dbid:
				role = info["roleType"]
				break

		avatar.cellData["modelID"] = d_avatar_inittab.datas[role]["modelID"]
		avatar.cellData["modelScale"] = d_avatar_inittab.datas[role]["modelScale"]
		avatar.cellData["moveSpeed"] = d_avatar_inittab.datas[role]["moveSpeed"]
		avatar.accountEntity = self
		self.activeCharacter = avatar
		self.giveClientTo(avatar)
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
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

