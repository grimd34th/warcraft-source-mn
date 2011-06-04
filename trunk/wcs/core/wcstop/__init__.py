import es

from es import getuserid, exists
from popuplib import create, send
import wcs

popups = []


def doCommand(userid, args='wcstop'):
	if len(wcs.wcs.database) < 5:
		#tell(userid, '#multi', wcs.wcs.strings('wcstop: not enough', {}, wcs.wcs.getPlayer(userid).lang))
		wcs.wcs.tell(userid, 'wcstop: not enough')
		return

	if args == 'wcstop':
		args = 'wcstop5'

	positionsearch = int(args.replace('wcstop', '').strip())

	allplayers = list(wcs.wcs.database.ranks)

	del allplayers[:positionsearch - 5]
	del allplayers[positionsearch:]

	if len(allplayers):
		pname = 'top_%s_%s'%(userid, positionsearch)
		popups.append(pname)
		top = create(pname)

		top.addline('WCS top '+str(positionsearch))

		top.addline(' ')
		top.menuselect = callBack

		for number, steamid in enumerate(allplayers):
			if number < 5:
				wcs.wcs.database.execute("SELECT UserID, name, totallevel, currace FROM Players WHERE steamid = ?", (steamid, ))
				v = wcs.wcs.database.fetchall()
				if v:
					UserID, name, totallevel, currace = v[0]

					wcs.wcs.database.execute("SELECT level FROM Races WHERE UserID = ? AND name = ?", (UserID, currace))
					level = wcs.wcs.database.fetchone()

					top.addline('->'+str(positionsearch-5+number+1)+'. '+str(name))
					top.addline('  Total level '+str(totallevel)+', playing '+str(currace)+' level '+str(level))
				else:
					top.addline('Error when trying to fetch steamid '+str(steamid))
			else:
				break

		top.addline(' ')
		if positionsearch < 6:
			top.addline(' ')
		else:
			top.addline('->8. Back')

		if len(wcs.wcs.database) < positionsearch:
			top.addline(' ')
		else:
			top.addline('->9. Next')

		top.addline('0. Close')

		for x in xrange(1, 8):
			top.submenu(x, pname)

		top.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")

def popupHandler(userid, choice, popupid):
	last_split = popupid.split('_')
	last_search = int(last_split[2])

	if choice == 8:
		if last_search < 0:
			doCommand(userid, 'wcstop5')

		elif last_search < 6:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)-5
			doCommand(userid, 'wcstop%s'%newsearch)

	elif choice == 9:
		if last_search >= len(wcs.wcs.database):
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)+5
			doCommand(userid, 'wcstop%s'%newsearch)

def wcsRank(userid, args='wcsrank'):
	something = args.replace('wcsrank', '').strip()
	target = userid
	if len(something):
		target = getuserid(something)
		if not exists('userid', target):
			target = userid

	player = wcs.wcs.getPlayer(target)

	player.showRank()


callBack = popupHandler

def getPopups():
	return popups
