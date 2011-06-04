from es import exists
from cmdlib import registerServerCommand, unregisterServerCommand
from playerlib import getUseridList, getPlayer
from wcs.wcs import logging, strings, tell

def load():
	registerServerCommand('wcs_xtell', register, 'Syntax: wcs_xtell <userid> <text> <[arg]> <[value]>...')

def unload():
	unregisterServerCommand('wcs_xtell')

def register(args):
	if len(args) >= 2:
		userid   = str(args[0])
		text     = str(args[1])

		if userid.startswith('#'):
			userid = getUseridList(userid)
		else:
			userid = (userid, )

		hmm = []
		if len(args) >= 4:
			hmm = args[2:]

		tokens = {}
		for x in xrange(0, len(hmm), 2):
			try:
				tokens[hmm[x]] = hmm[x+1]
			except IndexError:
				logging.log('xtell: Error: Syntax: Not enough parameters.')
				logging.log('xtell: Information: Got: wcs_xtell '+' '.join(map(str, args)), 1)
				return

		for user in userid:
			if exists('userid', user):
				tell(user, text, tokens)
			else:
				logging.log('xtell: Information: Unknown userid: '+str(user))
				logging.log('xtell: Information: Args: wcs_xtell '+' '.join(map(str, args)))
	else:
		logging.log('xtell: Error: Syntax: wcs_xtell <userid> <text> <[arg]> <[value]>...')
		logging.log('xtell: Information: Got: wcs_xtell '+' '.join(map(str, args)), 1)
