import es
from popuplib import easymenu, create
import wcs

popups = []


def doCommand(userid):
	if es.exists('userid', userid):
		pname = 'playerinfo'+str(userid)
		popups.append(pname)
		popup = easymenu(pname, '_popup_choice', callBack)
		popup.settitle('Page')

		popup.c_beginsep = None
		popup.c_pagesep = None

		for user in es.getUseridList():
			popup.addoption(user, es.getplayername(user))

		popup.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("pending/pending")

def popupHandler(userid, target, popupid):
	if es.exists('userid', target):
		pname = 'playerinfo1'+str(userid)
		popups.append(pname)
		popup = create(pname)
		popup.menuselect = playerinfoselection

		player = wcs.wcs.getPlayer(target)
		popup.addline('->1. '+str(es.getplayername(target)))
		popup.addline('-'*25)
		popup.addline('o Total level '+str(player.player.totallevel))
		popup.addline('-'*25)
		popup.addline('o '+str(player.player.currace)+': Level '+str(player.race.level))

		race = wcs.wcs.racedb.getRace(player.player.currace)
		name = race['skillnames'].split('|')

		skills = player.race.skills.split('|')
		for skill, level in enumerate(skills):
			popup.addline(' - '+name[skill]+': '+str(level))

		popup.addline('-'*25)

		popup.addline('->8. Previous')
		popup.addline(' ')
		popup.addline('0. Close')

		for x in xrange(1, 8):
			popup.submenu(x, pname)

		popup.submenu(9, pname)

		popup.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")
	else:
		es.tell(userid, 'Unknown player')
		doCommand(userid)

def playerinfoselection(userid, choice, popupid):
	if choice == 8:
		doCommand(userid)


callBack = popupHandler

def getPopups():
	return popups
