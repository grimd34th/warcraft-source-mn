import es
from es import exists
from popuplib import create
import wcs

popups = []


def doCommand(userid):
	if exists('userid', userid):
		pname = 'spendskills_%s'%userid
		player = wcs.wcs.getPlayer(userid)
		unused = player.race.unused
		if unused:
			race = player.player.currace
			skills = player.race.skills.split('|')
			db = wcs.wcs.racedb.getRace(race)
			nol = int(db['numberoflevels'])

			if len(filter(lambda x: int(x) < nol, skills)):
				popups.append(pname)
				spendskills = create(pname)

				spendskills.menuselect = callBack

				spendskills.addline('You can spend points for the following '+race+' skills')

				skillnames  = db['skillnames'].split('|')
				skillneeded = db['skillneeded'].split('|')

				added = 0
				for number, skill in enumerate(skills):
					added += 1
					if int(skill) >= nol:
						spendskills.addline(str(number+1)+'. '+str(skillnames[number])+' (maxed)')
						spendskills.submenu(number+1, pname)
					else:
						if int(skillneeded[number]) > player.race.level:
							spendskills.addline(str(number+1)+'. '+str(skillnames[number])+' (need level '+skillneeded[number]+')')
							spendskills.submenu(number+1, pname)
						else:
							spendskills.addline('->'+str(number+1)+'. '+str(skillnames[number])+': '+str(skills[number])+' > '+str(int(skills[number])+1))

				while added < 9:
					spendskills.addline(' ')
					added += 1
					spendskills.submenu(added, pname)

				spendskills.addline(' ')
				spendskills.addline(' ')
				spendskills.addline('Unused Points: '+str(player.race.unused))

				spendskills.addline('0. Close')

				spendskills.send(userid)
				es.ServerVar('wcs_ppuser').set(userid)
				es.doblock("wcs/tools/pending/pending")
			else:
				wcs.wcs.tell(userid, 'spendskills: maximum level')
		else:
			wcs.wcs.tell(userid, 'spendskills: no unused')

def popupHandler(userid, choice, popupid):
	if choice < 10:
		player = wcs.wcs.getPlayer(userid)
		race   = player.player.currace
		db     = wcs.wcs.racedb.getRace(race)
		nos    = int(db['numberofskills'])
		nol    = int(db['numberoflevels'])
		needed = db['skillneeded'].split('|')

		if nos >= choice:
			skills = player.race.skills.split('|')
			if int(skills[choice-1]) < nol and int(needed[choice-1]) <= player.race.level:
				level = player.race.addPoint(choice)

				wcs.wcs.tell(userid, 'spendskills: upgrade skill', {'skill':db['skillnames'].split('|')[choice-1],'level':level})

				if player.race.unused:
					doCommand(userid)


callBack = popupHandler

def getPopups():
	return popups
