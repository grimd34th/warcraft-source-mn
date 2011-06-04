import es
from popuplib import create
import wcs

popups = []


def doCommand(userid):
	userid = str(userid)
	player = wcs.wcs.getPlayer(userid)

	pname = 'wcs_showskills_'+userid
	popups.append(pname)

	popup = create(pname)

	popup.addline('Your '+str(player.player.currace)+' skills:')

	skills = player.race.skills.split('|')
	names = player.race.racedb['skillnames'].split('|')
	n = 0

	while n < len(skills):
		level = str(skills[n])
		name = str(names[n])

		n += 1
		popup.addline('->'+str(n)+'. '+name+': '+level)

	popup.addline(' ')
	popup.addline(' ')

	popup.addline('Unused points: '+str(player.race.unused))

	for x in xrange(1, 9):
		popup.submenu(x, pname)

	popup.send(userid)
	es.ServerVar('wcs_ppuser').set(userid)
	es.doblock("wcs/tools/pending/pending")

def getPopups():
	return popups
