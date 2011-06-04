import es
import gamethread

from wcs import wcs



def player_spawn(ev):
	player_death({'userid':ev['userid']})
	gamethread.delayedname(1, 'wcs_showinfo'+ev['userid'], showHint, ev['userid'])

def player_death(ev):
	gamethread.cancelDelayed('wcs_showinfo'+ev['userid'])

def player_disconnect(ev):
	player_death({'userid':ev['userid']})

def showHint(userid):
	#There's no need to send it to bots
	if not es.getplayersteamid(userid) == 'BOT':
		p = wcs.getPlayer(userid)

		race = p.player.currace
		totallevel = p.player.totallevel
		level = p.race.level
		xp = p.race.xp
		needed = int(wcs.cfgdata['interval'])*level if level else int(wcs.cfgdata['interval'])
		rank = wcs.database.getRank(es.getplayersteamid(userid))

		text = str(race)+'\n----------\nTotallevel: '+str(totallevel)+'\nLevel: '+str(level)+'\nXp: '+str(xp)+'/'+str(needed)+'\n----------\nWCS rank: '+str(rank)+'/'+str(len(wcs.database))

		wcs.expand.keyHint(userid, text)

		player_spawn({'userid':userid})
