import es
from cmdlib import registerServerCommand, unregisterServerCommand
from playerlib import getPlayer
from gamethread import delayed
from weaponlib import getWeaponList
from UserDict import UserDict
from wcs.wcs import logging, tell, restrict

def load():
	registerServerCommand('wcs_xrestrict', register, 'Syntax: wcs_xrestrict <restrict/allow> <userid> <weapon>')
	es.addons.registerClientCommandFilter(cc_filter)

def unload():
	unregisterServerCommand('wcs_xrestrict')
	es.addons.unregisterClientCommandFilter(cc_filter)

def register(args):
	if len(args) == 3:
		todo = str(args[0])
		userid = str(args[1])
		weapons = restrict.weaponw(args[2])

		if es.exists('userid', userid):
			if todo == 'restrict':
				if weapons.startswith('#'):
					for weapon in getWeaponList(weapons):
						restrict.restrict(userid, weapon)
				else:
					restrict.restrict(userid, weapons)

			elif todo == 'allow':
				if weapons.startswith('#'):
					for weapon in getWeaponList(weapons):
						restrict.allow(userid, weapon)
				else:
					restrict.allow(userid, weapons)
			else:
				logging.log('xrestrict: Error: Syntax: wcs_xrestrict <restrict/allow> <userid> <weapon>')
				logging.log('xrestrict: Error: Got: wcs_xrestrict '+' '.join(map(str, args)), 1)
		else:
			logging.log('xrestrict: Information: Unknown userid: '+userid)
			logging.log('xrestrict: Information: Args: wcs_xrestrict '+' '.join(map(str, args)))
	else:
		logging.log('xrestrict: Error: Syntax: wcs_xrestrict <restrict/allow> <userid> <weapon>')
		logging.log('xrestrict: Error: Got: wcs_xrestrict '+' '.join(map(str, args)), 1)

def cc_filter(userid, args):
	userid = str(userid)
	if userid in restrict.restrictData:
		if args[0].lower() == 'buy' and len(args) > 1:
			weapon = args[1]
			if args[1].lower() == 'mp5':
				weapon = restrict.weaponw('weapon_mp5navy')

			weapon = restrict.weaponw(weapon)
			if weapon in restrict.restrictData[userid]:
				if restrict.restrictData[userid][weapon]:
					tell(userid, 'xrestrict: restricted')
					return False
	return True



def player_activate(ev):
	userid = str(ev['userid'])
	if not userid in restrict.restrictData:
		restrict.restrictData[userid] = {}

def player_disconnect(ev):
	userid = str(ev['userid'])
	if userid in restrict.restrictData:
		del restrict.restrictData[userid]

def player_death(ev):
	player_disconnect(ev)

def item_pickup(ev):
	userid = str(ev['userid'])
	if userid in restrict.restrictData:
		item = restrict.weaponw(ev['item'])
		if item in restrict.restrictData[userid]:
			if restrict.restrictData[userid][item]:
				restrict.remove(userid, item)
