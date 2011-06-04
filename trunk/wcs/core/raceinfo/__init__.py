import es
from popuplib import create, exists, send
import wcs


popups = []


def doCommand(userid, args='raceinfo', race=True, count=(0,3)):
	if es.exists('userid', userid):
		if args == 'raceinfo':
			args = 'raceinfo0'

		positionsearch = str(args.replace('raceinfo', '').strip())

		if len(positionsearch):
			if positionsearch.isdigit():
				positionsearch = int(positionsearch)
			else:
				positionsearch = 0
		else:
			positionsearch = 0

		allraces = wcs.wcs.racedb.getAll().keys()

		if race:
			try:
				race = allraces[positionsearch]
			except IndexError:
				race = allraces[-1]
		else:
			race = wcs.wcs.getPlayer(userid).player.currace
			positionsearch = wcs.wcs.racedb.index(race)

		currace = wcs.wcs.racedb.getRace(race)

		pname = 'raceinfo_'+str(positionsearch)+'_'+str(count[0])
		if not exists(pname):
			popups.append(pname)
			raceinfo = create(pname)

			raceinfo.menuselect = callBack

			raceinfo.addline('->'+str(allraces.index(race)+1)+'.      '+race+' ('+str(currace['numberoflevels'])+' levels/'+str(currace['numberofskills'])+' skills)')
			if int(currace['required']):
				raceinfo.addline('Required level: '+str(currace['required']))
			if int(currace['maximum']):
				raceinfo.addline('Maximum level: '+str(currace['maximum']))
			if 'allowonly' in currace and len(currace['allowonly']):
				raceinfo.addline('<Private race>')
			if 'author' in currace and len(currace['author']):
				raceinfo.addline('Credits '+str(currace['author']))

			raceinfo.addline(' ')
			raceinfo.addline(' ')

			name = currace['skillnames'].split('|')[count[0]:count[1]]
			desc = currace['skilldescr'].split('|')[count[0]:count[1]]
			number = 1
			#while number <= int(currace['numberofskills']):
			while number <= len(name):
				try:
					v = str(name[number-1]).split('\\n')
					raceinfo.addline('->'+str(number)+'. '+v[0])
					for x in v[1:]:
						raceinfo.addline('->'+x)
				except IndexError:
					wcs.wcs.logging.log('raceinfo: Error: Race '+race+' is missing a skill name')
					raceinfo.addline('-> ERROR!')
					raceinfo.addline('-> Report this to the server owner!')

				try:
					v = str(desc[number-1]).split('\\n')
					for x in v:
						raceinfo.addline(x)
				except IndexError:
					wcs.wcs.logging.log('raceinfo: Error: Race '+race+' is missing a skill name')
					raceinfo.addline('-> ERROR!')
					raceinfo.addline('-> Report this to the server owner!')

				number += 1

			while number <= 4:
				raceinfo.addline(' ')
				raceinfo.submenu(number, pname)
				number += 1

			if not count[0]:
				raceinfo.addline(' ')
				raceinfo.submenu(6, pname)
			else:
				raceinfo.addline('->6. Previous Part')
			if count[1] == 9:
				raceinfo.addline(' ')
				raceinfo.submenu(7, pname)
			else:
				raceinfo.addline('->7. Next Part')

			if allraces.index(race) == 0:
				raceinfo.addline(' ')
				raceinfo.submenu(8, pname)
			else:
				raceinfo.addline('->8. Back')

			try:
				hmm = allraces[allraces.index(race)+1]
				raceinfo.addline('->9. Next')
			except IndexError:
				raceinfo.addline(' ')
				raceinfo.submenu(9, pname)

			number = 1
			while number < 7:
				raceinfo.submenu(number, pname)
				number += 1

			raceinfo.addline('0. Close')

			#raceinfo.send(userid)

		send(pname, userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")


def popupHandler(userid, choice, popupid):
	last_split  = popupid.split('_')
	last_search = int(last_split[1])
	count = int(last_split[2])

	if choice == 6:
		if count == 6:
			doCommand(userid, 'raceinfo%s'%last_search, count=(3,6))
		elif count == 3:
			doCommand(userid, 'raceinfo%s'%last_search, count=(0,3))

	elif choice == 7:
		if count == 3:
			doCommand(userid, 'raceinfo%s'%last_search, count=(6,9))
		elif count == 0:
			doCommand(userid, 'raceinfo%s'%last_search, count=(3,6))

	elif choice == 8:
		#if last_search < 0:
		#	doCommand(userid, 'raceinfo0')

		if last_search:
			newsearch = int(last_search)-1
			doCommand(userid, 'raceinfo%s'%newsearch)

	elif choice == 9:
		if last_search < len(wcs.wcs.racedb.getAll().keys())-1:
			newsearch = int(last_search)+1
			doCommand(userid, 'raceinfo%s'%newsearch)




callBack = popupHandler

def getPopups():
	return popups
