"""
"""
from KBEDebug import *
import d_items

from items.ItemConsume import ItemConsume
from items.ItemEquip import ItemEquip

_g_items = {}

def onInit():
	"""
	init items.
	"""
	for key, datas in d_items.datas.items():
		script = datas['script']
		scriptinst = eval(script)()
		_g_items[key] = scriptinst
		scriptinst.loadFromDict(datas)
		
def getItem(itemID):
	return _g_items.get(itemID)