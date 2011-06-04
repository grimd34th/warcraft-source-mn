from es import tell
import wcs


def doCommand(userid):
	player = wcs.wcs.getPlayer(userid)

	if filter(lambda x: int(x), player.race.skills.split('|')):
		'''skills = player.race.skills.split('|')'''
		race = player.player.currace
		raceinfo = wcs.wcs.racedb.getRace(race)
		skills = int(raceinfo['numberofskills'])
		levels = int(raceinfo['numberoflevels'])

		level = player.race.level
		unused = player.race.unused

		maxunused = skills*levels
		v = 0
		for x in player.race.skills.split('|'):
			v += int(x)
		unused += v

		if maxunused <= unused:
			playerunused = maxunused
		else:
			playerunused = unused

		'''for x in skills:
			levels += int(x)'''

		player.race.unused = playerunused
		player.race.skills = ''
		player.race.save()

		player.race.refresh()

		wcs.wcs.tell(userid, 'resetskills: resetted', {'unused':player.race.unused})
