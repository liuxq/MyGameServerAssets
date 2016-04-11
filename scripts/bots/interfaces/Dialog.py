# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class Dialog:
	def __init__(self):
		pass

	def dialog_setContent(self, arg1, arg2, arg3, arg4,arg5,arg6):
		"""
		defined method.
		"""
		DEBUG_MSG("Dialog:dialog_addOption::dialogType=%i, dialogKey=%i, title=%s, extra=%s" % \
				(arg1, arg2, arg3, arg4))
	
	def dialog_close(self):
		"""
		defined method.
		"""
		DEBUG_MSG("Dialog:dialog_close:: %i" % (self.id))
				

