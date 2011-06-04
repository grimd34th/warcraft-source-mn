from es import exists
from wcs.wcs import CfgManager, getPlayer, strings, tell

cfg = CfgManager('freelevels')
levels = int(cfg.cvar('wcs_freelevels', 25, 'Amount of levels the players gain when they have 0 in totallevel.'))

cfg.write()

def load():
	cfg.execute()

def player_activate(ev):
	userid = ev['userid']
	if exists('userid', userid):
		player = getPlayer(userid)
		if not player.player.totallevel:
			player.giveLevel(levels)
			tell(userid, 'freelevels: gained', {'levels':levels})
