from playerlib import getPlayerList
from wcs.wcs import getPlayer, CfgManager, checkEvent, shopmenu

cfg = CfgManager('ext_dod')

tickpoint				= cfg.cvar('wcs_cfg_tickpointxp',				10, 'XP gained for rescuing a hostage')
roundwin				= cfg.cvar('wcs_cfg_roundwinxp',				30, 'XP gained for defusing the bomb')
defusexp				= cfg.cvar('wcs_cfg_defusexp',				30, 'XP gained for defusing the bomb')
plantxp					= cfg.cvar('wcs_cfg_plantxp',				15, 'XP gained for planting the bomb')
explodexp				= cfg.cvar('wcs_cfg_explodexp',				15, 'XP gained for making the bomb explode')

allow_bomb_defused		= cfg.cvar('wcs_cfg_allow_bomb_defused',	0,  'Allow the bomb_defused event for races and items (1 = ON, 0 = OFF)')
allow_bomb_planted		= cfg.cvar('wcs_cfg_allow_bomb_planted',	0,  'Allow the bomb_planted event for races and items (1 = ON, 0 = OFF)')
allow_bomb_exploded		= cfg.cvar('wcs_cfg_allow_bomb_exploded',	0,  'Allow the bomb_exploded event for races and items (1 = ON, 0 = OFF)')

cfg.write()

def load():
	cfg.execute()

def dod_tick_points(ev):
	for user in getPlayerList('#t' if int(ev['team']) == 2 else '#ct'):
		getPlayer(user.userid).giveXp(tickpoint)

def dod_round_win(ev):
	for user in getPlayerList('#t' if int(ev['team']) == 2 else '#ct'):
		getPlayer(user.userid).giveXp(roundwin)

def dod_bomb_planted(ev):
	userid = ev['userid']

	getPlayer(userid).giveXp(defusexp)

	if allow_bomb_defused:
		checkEvent(userid, 'bomb_planted')
		shopmenu.checkEvent(userid, 'bomb_planted')

def dod_bomb_defused(ev):
	userid = ev['userid']

	getPlayer(userid).giveXp(plantxp)

	if allow_bomb_planted:
		checkEvent(userid, 'bomb_defused')
		shopmenu.checkEvent(userid, 'bomb_defused')

def dod_bomb_exploded(ev):
	for userid in getPlayerList('#t'):
		getPlayer(userid).giveXp(int(explodexp))

	userid = ev['userid']

	if allow_bomb_exploded:
		checkEvent(userid, 'bomb_exploded')
		shopmenu.checkEvent(userid, 'bomb_exploded')