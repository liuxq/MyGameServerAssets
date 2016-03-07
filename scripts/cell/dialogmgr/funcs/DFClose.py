# -*- coding: utf-8 -*-
#
"""
"""
from KBEDebug import *
from dialogmgr.funcs.iDFunction import iDFunction

class DFClose(iDFunction):
	"""
	"""
	def __init__(self, args):
		pass
		
	def valid(self, avatar, talker):
		return True

	def do(self, avatar, talker):
		avatar.client.dialog_close()
		return True