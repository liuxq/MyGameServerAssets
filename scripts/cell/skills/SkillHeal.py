# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import * 
from skills.base.SkillInitiative import SkillInitiative

class SkillHeal(SkillInitiative):
	def __init__(self):
		SkillInitiative.__init__(self)

	def canUse(self, caster, scObject):
		"""
		virtual method.
		可否使用 
		@param caster: 使用技能者
		@param receiver: 受技能影响者
		"""
		return SkillInitiative.canUse(self, caster, scObject)
		
	def use(self, caster, scObject):
		"""
		virtual method.
		使用技能
		@param caster: 使用技能者
		@param receiver: 受技能影响者
		"""
		return SkillInitiative.use(self, caster, scObject)
		
	def receive(self, caster, receiver):
		"""
		virtual method.
		可以对受术者做一些事情了
		"""
		attack = random.randint(caster.attack_Min, caster.attack_Max)
		defence = receiver.defence
		if self.getID() == 3:
			damage = attack + 10

		receiver.recvDamage(caster.id, self.getID(), 0, -damage)