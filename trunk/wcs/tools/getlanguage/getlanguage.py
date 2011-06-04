from es import exists, ServerVar
from cmdlib import registerServerCommand, unregisterServerCommand
from playerlib import getPlayer
from wcs.wcs import logging, strings

def load():
	registerServerCommand('wcs_getlanguage', register, 'Syntax: wcs_getlanguage <var> <userid> <text>')

def unload():
	unregisterServerCommand('wcs_getlanguage')

def register(args):
	if len(args) == 3:
		var    = str(args[0])
		userid = str(args[1])
		text   = str(args[2])

		if exists('userid', userid):
			ServerVar(var).set(strings(text, {}, getPlayer(userid).get('lang')))
		elif userid == 'en':
			ServerVar(var).set(strings(text, {}, 'en'))
		else:
			logging.log('getlanguage: Information: Unknown userid: '+userid)
			logging.log('getlanguage: Information: Args: wcs_getlanguage '+' '.join(map(str, args)))
	else:
		logging.log('getlanguage: Error: Syntax: wcs_getlanguage <var> <userid> <text>')
		logging.log('getlanguage: Information: Got: wcs_getlanguage '+' '.join(map(str, args)), 1)
