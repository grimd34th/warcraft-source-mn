from es import centertell, exists
from cmdlib import registerServerCommand, unregisterServerCommand
from playerlib import getPlayer, getPlayerList
from wcs.wcs import strings, logging



def load():
	registerServerCommand('wcs_xcentertell', register, 'Syntax: wcs_xcentertell <userid> <text> <[arg]> <[value]>...')

def unload():
	unregisterServerCommand('wcs_xcentertell')

def register(args):
	if len(args) >= 2:
		userid = str(args[0])
		text = str(args[1])

		if userid.startswith('#'):
			userid = getPlayerList(userid)

		if not hasattr(userid, '__iter__'):
			if not exists('userid', userid):
				logging.log('xcenter: Information: Unknown userid: '+userid)
				logging.log('xcenter: Information: Args: wcs_xcentertell '+' '.join(map(str, args)))
				return

			userid = (getPlayer(userid), )

		hmm = []
		if len(args) >= 4:
			hmm = args[2:]

		tokens = {}
		for x in xrange(0, len(hmm), 2):
			try:
				tokens[hmm[x]] = hmm[x+1]
			except IndexError:
				logging.log('xcenter: Error: Syntax: Not enough parameters.')
				logging.log('xcenter: Information: Got: wcs_xcentertell '+' '.join(map(str, args)), 1)
				return

		for user in userid:
			if exists('userid', user):
				centertell(user, strings(text, tokens, user.get('lang')))
			else:
				logging.log('xcenter: Information: Unknown userid: '+userid)
				logging.log('xcenter: Information: Args: wcs_xcentertell '+' '.join(map(str, args)))
	else:
		logging.log('xcenter: Error: Syntax: wcs_xcentertell <userid> <text> <[arg]> <[value]>...')
		logging.log('xcenter: Information: Got: wcs_xcentertell '+' '.join(map(str, args)), 1)
