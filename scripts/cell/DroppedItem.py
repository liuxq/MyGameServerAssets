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
		