import es
from popuplib import create, exists, send

import wcs
from wcs.core import changerace
reload(changerace)

from wcs.core import raceinfo
reload(raceinfo)

from wcs.core import spendskills
reload(spendskills)

from wcs.core import resetskills
reload(resetskills)

from wcs.core import shopmenu
reload(shopmenu)

from wcs.core import shopinfo
reload(shopinfo)

from wcs.core import showskills
reload(showskills)

from wcs.core import wcstop
reload(wcstop)

from wcs.core import playerinfo
reload(playerinfo)

from wcs.core import shopmenu
reload(shopmenu)

from wcs.core import shopinfo
reload(shopinfo)


popups = []

def doCommand(userid):
	pname = 'wcsmenu'
	if not exists(pname):
		popups.append(pname)
		popup = create(pname)

		popup.menuselect = callBack

		popup.addline('- WCSmenu -')
		popup.addline('->1. shopmenu - buy shop items')
		popup.addline('->2. shopinfo    - show item info')
		popup.addline('-------------------')
		popup.addline('->3. showskills  - show all skills levels')
		popup.addline('->4. resetskills  - reset your skills')
		popup.addline('->5. spendskills - spend skill points')
		popup.addline('-------------------')
		popup.addline('->6. changerace - choose your race')
		popup.addline('->7. raceinfo      - show info about skills')
		popup.addline('-------------------')
		popup.addline('->8. playerinfo   - shows info about a player')
		popup.addline('->9. wcstop        - WCS top10')
		popup.addline('-------------------')
		popup.addline(' ')
		popup.addline('0. Close')

		#popup.send(userid)

	send(pname, userid)
	es.ServerVar('wcs_ppuser').set(userid)
	es.doblock("wcs/tools/pending/pending")

command = {1:(shopmenu.doCommand, 0),
		   2:(shopinfo.doCommand, 0),
		   3:(showskills.doCommand, 0),
		   4:(resetskills.doCommand, 0),
		   5:(spendskills.doCommand, 0),
		   6:(changerace.doCommand, 'changerace'),
		   7:(raceinfo.doCommand, 'raceinfo'),
		   8:(playerinfo.doCommand, 0),
		   9:(wcstop.doCommand, 'wcstop')}

def popupHandler(userid, choice, popupid):
	if choice in command:
		place = command[choice]
		if place[1]:
			place[0](userid, place[1])
		else:
			place[0](userid)


callBack = popupHandler

def getPopups():
	return popups
