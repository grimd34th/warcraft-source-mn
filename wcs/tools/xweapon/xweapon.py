from es import ServerVar, dbgmsg
from cmdlib import registerServerCommand, unregisterServerCommand
from weaponlib import getWeapon
from wcs.wcs import logging

def load():
	registerServerCommand('wcs_xweapon', register, 'Syntax: wcs_xweapon <key> <var> <weapon>')

def unload():
	unregisterServerCommand('wcs_xweapon')

def register(args):
	if len(args) == 3:
		key = str(args[0])
		var = ServerVar(args[1])
		weapon = getWeapon(args[2])

		if hasattr(weapon, key):
			attr = getattr(weapon, key)

			if callable(attr):
				var.set(attr())
			else:
				var.set(attr)
		else:
			logging.log('xweapon: Error: Syntax: Unknown key: '+key)
			logging.log('xweapon: Information: Got: wcs_xweapon '+' '.join(map(str, args)))

	else:
		logging.log('xweapon: Error: Syntax: wcs_xweapon <key> <var> <weapon>')
		logging.log('xweapon: Information: Got: wcs_xweapon '+' '.join(map(str, args)))
