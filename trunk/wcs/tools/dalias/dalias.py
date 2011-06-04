from es import ServerVar, server
from cmdlib import registerServerCommand, unregisterServerCommand
from wcs.wcs import logging, aliass

def load():
	registerServerCommand('wcs_dalias', register, 'Syntax: wcs_dalias <alias> <value1> <[value2]> <[value3]> ...')

def unload():
	unregisterServerCommand('wcs_dalias')

def register(args):
	if len(args) > 1:
		if args[0] in aliass:
			number = 1
			while len(args) > number:
				ServerVar('wcs_tmp'+str(number)).set(args[number])
				number += 1

			#Run the alias.
			server.insertcmd(aliass[args[0]])
		else:
			logging.log('dalias: Error: Unknown alias: '+args[0])
			logging.log('dalias: Information: Got: wcs_dalias '+' '.join(map(str, args)), 1)
	else:
		logging.log('dalias: Error: Syntax: wcs_dalias <alias> <value1> <[value2]> <[value3]> ...')
		logging.log('dalias: Information: Got: wcs_dalias '+' '.join(map(str, args)), 1)
