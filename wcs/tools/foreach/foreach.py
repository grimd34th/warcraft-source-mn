from es import server, ServerVar
from cmdlib import registerServerCommand, unregisterServerCommand
from playerlib import getUseridList
from weaponlib import getWeaponList
from wcs.wcs import logging

def load():
	registerServerCommand('wcs_foreach', register, 'Syntax: wcs_foreach <player/weapon/token> <var> <identifier> <"command">')

def unload():
	unregisterServerCommand('wcs_foreach')

def register(args):
	if len(args) >= 1:
		target = str(args[0]).lower()

		if target == 'player':
			if len(args) >= 4:
				var = str(args[1])
				id  = str(args[2])
				cmd = ' '.join(args[3:])

				if id.startswith('#'):
					for user in getUseridList(id):
						server.insertcmd('es_xset '+var+' '+str(user)+';'+cmd)
				else:
					server.insertcmd('es_xset '+var+' '+id+';'+cmd)
			else:
				logging.log('foreach: Error: Syntax: wcs_foreach player <var> <identifier> <"command">')
				logging.log('foreach: Information: Got: wcs_foreach '+' '.join(map(str, args)), 1)

		elif target == 'weapon':
			if len(args) >= 4:
				var = str(args[1])
				id  = str(args[2])
				cmd = ' '.join(args[3:])

				for weapon in getWeaponList(id):
					server.insertcmd('es_xset '+var+' '+str(weapon)+';'+cmd)
			else:
				logging.log('foreach: Error: Syntax: wcs_foreach weapon <var> <identifier> <"command">')
				logging.log('foreach: Information: Got: wcs_foreach '+' '.join(map(str, args)), 1)

		elif target == 'token':
			if len(args) >= 5:
				var    = str(args[1])
				string = str(args[2])
				sep    = str(args[3])
				cmd    = ' '.join(args[3:])

				for token in string.split(sep):
					if len(token):
						server.insertcmd('es_xset '+var+' '+str(token)+';'+cmd)
			else:
				logging.log('foreach: Error: Syntax: wcs_foreach token <var> <string> <separator> <"command">')
				logging.log('foreach: Information: Got: wcs_foreach '+' '.join(map(str, args)), 1)

		else:
			logging.log('foreach: Error: Syntax: wcs_foreach <player/weapon/token> <var> <identifier> <"command">')
			logging.log('foreach: Information: Got: wcs_foreach '+' '.join(map(str, args)), 1)
	else:
		logging.log('foreach: Error: Syntax: wcs_foreach <player/weapon/token> <var> <identifier> <"command">')
		logging.log('foreach: Information: Got: wcs_foreach '+' '.join(map(str, args)), 1)
