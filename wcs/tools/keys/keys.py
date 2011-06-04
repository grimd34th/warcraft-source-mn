from es import exists, getUseridList, keygroupdelete, keygroupcreate, keydelete
from keyvalues import KeyValues, getKeyGroup


keygroup = None

def load():
	global keygroup
	keygroupcreate('WCSuserdata')
	keygroup = getKeyGroup('WCSuserdata')
	keygroup['WCSuserdata'] = KeyValues(name='WCSuserdata')

	for user in getUseridList():
		keygroup[str(user)] = KeyValues(name=str(user))

def unload():
	try:
		del keygroup
	except UnboundLocalError:
		keygroupdelete('WCSuserdata')

def player_spawn(ev):
	if not exists('key', 'WCSuserdata', ev['userid']):
		keygroup[ev['userid']] = KeyValues(name=ev['userid'])

def player_activate(ev):
	keygroup[ev['userid']] = KeyValues(name=ev['userid'])

def player_disconnect(ev):
	keydelete('WCSuserdata', ev['userid'])
