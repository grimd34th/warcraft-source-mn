import es
import playerlib
import wcs

def load():
	es.addons.registerClientCommandFilter(teamchange)

def unload():
	es.addons.unregisterClientCommandFilter(teamchange)

def teamchange(userid, args):
	if str(args[0]) == 'jointeam':
		race = wcs.wcs.getPlayer(userid).race.name
		
		raceinfo = wcs.wcs.racedb.getRace(race)
		
		team = int(args[1])
		teamlimit = raceinfo['teamlimit']
		count = len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == team, es.getUseridList())))
		es.ServerVar("wcs_count").set(count)
		if team in (2, 3) and 'teamlimit' in raceinfo and len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == team, es.getUseridList()))) >= int(raceinfo['teamlimit']) and not int(raceinfo['teamlimit']) == 0:
			es.tell(userid, "#multi", "#lightgreenSorry, your race has reached the #greenTeamlimit #lightgreenon the other team.")
			return False
	return True