from es import server
from cmdlib import registerServerCommand, unregisterServerCommand
from wcs.wcs import logging, aliass




def load():
	registerServerCommand('wcs_xalias', register, 'Syntax: wcs_xalias <alias> <["command"]>')

def unload():
	unregisterServerCommand('wcs_xalias')

def register(args):
	if len(args) >= 1:
		alias = str(args[0])
		if len(args) == 1:
			if alias in aliass:
				server.insertcmd(str(aliass[alias]))
			else:
				logging.log('xalias: Error: Unknown alias: '+alias)
		elif len(args) == 2:
			if alias in aliass:
				logging.log('xalias: Information: Alias '+alias+' does already exists. Overwriting...', 3)

			aliass[alias] = ' '.join(map(str, args[1:]))
		else:
			logging.log('xalias: Error: Syntax: wcs_xalias <alias> <["command"]>')
			logging.log('xalias: Information: Got: wcs_xalias '+' '.join(map(str, args)), 1)
	else:
		logging.log('xalias: Error: Syntax: wcs_xalias <alias> <["command"]>')
		logging.log('xalias: Information: Got: wcs_xalias '+' '.join(map(str, args)), 1)
