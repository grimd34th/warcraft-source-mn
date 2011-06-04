from es import exists
from playerlib import getPlayerList, getPlayer as gP
from wcs.wcs import getPlayer, CfgManager, checkEvent, shopmenu, strings

cfg = CfgManager('ext_cstrike')

hostagexp				= cfg.cvar('wcs_cfg_hostagexp',				10, 'XP gained for rescuing a hostage')
defusexp				= cfg.cvar('wcs_cfg_defusexp',				30, 'XP gained for defusing the bomb')
plantxp					= cfg.cvar('wcs_cfg_plantxp',				15, 'XP gained for planting the bomb')
explodexp				= cfg.cvar('wcs_cfg_explodexp',				15, 'XP gained for making the bomb explode')

allow_hostage_rescued	                = cfg.cvar('wcs_cfg_allow_hostage_rescued',	0,  'Allow the hostage_rescued event for races and items (1 = ON, 0 = OFF)')
allow_bomb_defused	                = cfg.cvar('wcs_cfg_allow_bomb_defused',	0,  'Allow the bomb_defused event for races and items (1 = ON, 0 = OFF)')
allow_bomb_planted	                = cfg.cvar('wcs_cfg_allow_bomb_planted',	0,  'Allow the bomb_planted event for races and items (1 = ON, 0 = OFF)')
allow_bomb_exploded	                = cfg.cvar('wcs_cfg_allow_bomb_exploded',	0,  'Allow the bomb_exploded event for races and items (1 = ON, 0 = OFF)')
allow_player_flashexplode	        = cfg.cvar('wcs_cfg_allow_player_flashexplode',	0,  'Allow the player_flashexplode event for races and items (1 = ON, 0 = OFF)')
allow_player_heexplode	                = cfg.cvar('wcs_cfg_allow_player_heexplode',	0,  'Allow the player_heexplode event for races and items (1 = ON, 0 = OFF)')
allow_player_smokeexplode	        = cfg.cvar('wcs_cfg_allow_player_smokeexplode',	0,  'Allow the player_smokeexplode event for races and items (1 = ON, 0 = OFF)')

cfg.write()

def load():
	cfg.execute()

def hostage_rescued(ev):
	userid = ev['userid']
	if exists('userid', userid):
		getPlayer(userid).giveXp(int(hostagexp), strings('cstrike: rescuing a hostage', {}, gP(userid).lang))

		if allow_hostage_rescued:
			checkEvent(userid, 'hostage_rescued')
			shopmenu.checkEvent(userid, 'hostage_rescued')

def bomb_defused(ev):
	userid = ev['userid']
	if exists('userid', userid):
		getPlayer(ev['userid']).giveXp(int(defusexp), strings('cstrike: defusing the bomb', {}, gP(userid).lang))

		if allow_bomb_defused:
			checkEvent(userid, 'bomb_defused')
			shopmenu.checkEvent(userid, 'bomb_defused')

def bomb_planted(ev):
	userid = ev['userid']
	if exists('userid', userid):
		getPlayer(ev['userid']).giveXp(int(plantxp), strings('cstrike: planting the bomb', {}, gP(userid).lang))

		if allow_bomb_planted:
			checkEvent(userid, 'bomb_planted')
			shopmenu.checkEvent(userid, 'bomb_planted')

def bomb_exploded(ev):
	for userid in getPlayerList('#t'):
		getPlayer(userid).giveXp(int(explodexp), strings('cstrike: making the bomb explode', {}, gP(userid).lang))

	userid = ev['userid']

	if exists('userid', userid):
		if allow_bomb_exploded:
			checkEvent(userid, 'bomb_exploded')
			shopmenu.checkEvent(userid, 'bomb_exploded')

def flashbang_explode(ev):
	userid = ev['userid']
	if exists('userid', userid):

		if allow_player_flashexplode:
			checkEvent(userid, 'player_flashexplode')
			shopmenu.checkEvent(userid, 'player_flashexplode')

def hegrenade_explode(ev):
	userid = ev['userid']
	if exists('userid', userid):

		if allow_player_heexplode:
			checkEvent(userid, 'player_heexplode')
			shopmenu.checkEvent(userid, 'player_heexplode')

def smokegrenade_explode(ev):
	userid = ev['userid']
	if exists('userid', userid):

		if allow_player_smokeexplode:
			checkEvent(userid, 'player_smokeexplode')
			shopmenu.checkEvent(userid, 'player_smokeexplode')
