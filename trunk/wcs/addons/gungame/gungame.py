from es import exists
from wcs.wcs import logging, getPlayer, ini, strings, CfgManager


cfg = CfgManager('gungame')


cfg.text("""
// ****************************
// ****************************
// ******** XP SETTINGS *******
// ****************************
// ****************************""", False)

levelup				= cfg.cvar('wcs_gg_levelup',		10,		'XP gained for level up')
knifesteal			= cfg.cvar('wcs_gg_knife_steal',	25,		'XP gained for steal a level')
multilevel			= cfg.cvar('wcs_gg_multi_level',	15,		'XP gained for multi leveling')
newleader			= cfg.cvar('wcs_gg_new_leader',		15,		'XP gained for become the new leader')
win					= cfg.cvar('wcs_gg_win',			30,		'XP gained for win')

cfg.write()

def load():
	if not exists('variable', 'eventscripts_gg5') and not exists('variable', 'eventscripts_gg'):
		logging.log('gungame: Information: No GunGame found. Stopping progress...', 4)
		return

	cfg.execute()

def gg_levelup(ev):
	getPlayer(ev['attacker']).giveXp(int(levelup), strings('gungame: level up', {}, getPlayer(ev['attacker']).get('lang')))

def gg_knife_steal(ev):
	getPlayer(ev['attacker']).giveXp(int(knifesteal), strings('gungame: knife steal', {}, getPlayer(ev['attacker']).get('lang')))

def gg_multi_level(ev):
	getPlayer(ev['leveler']).giveXp(int(multilevel), strings('gungame: multi level', {}, getPlayer(ev['leveler']).get('lang')))

def gg_new_leader(ev):
	getPlayer(ev['leveler']).giveXp(int(newleader), strings('gungame: new leader', {}, getPlayer(ev['leveler']).get('lang')))

def gg_win(ev):
	getPlayer(ev['attacker']).giveXp(int(win), strings('gungame: win', {}, getPlayer(ev['attacker']).get('lang')))
