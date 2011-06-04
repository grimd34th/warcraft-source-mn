from popuplib import create, send, exists


popups = []

def _create():
	popup = create('wcs_welcome')
	popups.append('wcs_welcome')
	popup.addline('WCS - Warcraft:Source')
	popup.addline(' ')
	popup.addline('->1. What\'s that ?')
	popup.addline('WCS is a CS:S modification script, similar to WC3:FT for CS 1.6.')
	popup.addline('All effects and changes in gameplay are part of WCS,')
	popup.addline('they are (in most cases) not cheats or hacks.')
	popup.addline(' ')
	popup.addline('->2. How to play ?')
	popup.addline('First, \'wcshelp\' shows all the commands.')
	popup.addline('You can select a race, gain XP, spend points for skills')
	popup.addline('or money for shop items.')
	popup.addline('For details, say \'raceinfo\' or \'shopinfo\'.')
	popup.addline(' ')
	popup.addline('->3. Have fun !')
	popup.addline(' ')
	popup.addline(' ')
	popup.addline(' ')
	popup.addline('Press 0 to close this.')
	for x in xrange(1, 10):
		popup.submenu(x, 'wcs_welcome')

def doCommand(userid):
	if not exists('wcs_welcome'):
		_create()

	send('wcs_welcome', userid)

def getPopups():
	return popups
