from cmdlib import registerServerCommand, unregisterServerCommand
from wcs.wcs import logging

def load():
	registerServerCommand('wcs_debug', register, 'Syntax: wcs_debug <level> <text>')

def unload():
	unregisterServerCommand('wcs_debug')

def register(args):
	if len(args):
		if str(args[0]).isdigit():
			logging.log(' '.join(args[1:]), int(args[0]))
		else:
			logging.log(' '.join(args))
