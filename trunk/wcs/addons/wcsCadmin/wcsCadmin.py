import es
import cmdlib
import popuplib
import playerlib

from wcs import wcs

from path import path
from configobj import ConfigObj


cfg = wcs.CfgManager('wcsCadmin')
cfgchangerace = cfg.cvar('wcs_wcscadmin_changerace_menu',       0, '0 = standard way, 1 = race categories')
cfgforceslay  = cfg.cvar('wcs_wcscadmin_force_changerace_slay', 1, 'Slay a player when forcing them to changerace')

cfg.write()

class scriptDatabase(object):
	def __init__(self):
		self.races = ConfigObj(path(wcs.ini.path).joinpath('ini').joinpath('scripts.ini'))

	def __contains__(self, item):
		return item in self.races['scripts']

	def __iter__(self):
		for x in self.races['scripts']:
			yield x
scriptdb = scriptDatabase()

class raceDatabase(object):
	def __init__(self):
		self.races = ConfigObj(path(wcs.ini.path).joinpath('ini').joinpath('racecat.ini'))

	def __contains__(self, item):
		return item in self.races

	def __iter__(self):
		for x in self.races:
			yield x

	def keys(self):
		return self.races.keys()

	def get(self, item):
		return self.races[item]
racedb = raceDatabase()




flags = ('wcscadmin_give_self',
		 'wcscadmin_give_players',
		 'wcscadmin_give_cash',
		 'wcscadmin_force_changerace',
		 'wcscadmin_settings',
		 'wcscadmin_players',
		 'wcscadmin_admins',
		 'wcscadmin_add_new_admin',
		 'wcscadmin_update_admin',
		 'wcscadmin_delete_admin')
popups = {}

def load():
	cfg.execute()

	p = popups['wcscadmin'] = popuplib.create('wcscadmin')
	p.addline('-WCS Custom Admin-')
	p.addline(' ')
	p.addline('->1. WCS Settings')
	p.addline('->2. Player Management')
	p.addline('->3. WCSadmin')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('0. Close')
	p.menuselect = WcscadminSelection
	for x in xrange(5, 10):
		p.submenu(x, 'wcscadmin')

	p = popups['wcssettings'] = popuplib.create('wcssettings')
	p.addline('-WCS Settings-')
	p.addline(' ')
	p.addline('->1. -Gained XP-')
	p.addline('->2. -Configure Races-')
	p.addline('->3. -Manage Races-')
	p.addline('->4. -Script Management-')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('->8. Back')
	p.addline(' ')
	p.addline('0. Close')
	p.menuselect = WcssettingsSelection
	for x in xrange(5, 10):
		p.submenu(x, 'wcssettings')
	p.submenu(8, 'wcscadmin')

	p = popups['wcsxpsettings0'] = popuplib.create('wcsxpsettings0')
	p.addline('-XP Settings-')
	p.addline(' ')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->1.Raise XP per Kill   +')
	p.addline('->2.Lower Xp per Kill   -')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->3.Raise XP per Head Shot   +')
	p.addline('->4.Lower Xp per Head Shot   -')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->5.Raise XP per Knife Kill   +')
	p.addline('->6.Lower Xp per Knife Kill   -')
	p.addline('-------------------')
	p.addline('->7. Default')
	p.addline('->8. Back')
	p.addline('->9. Next')
	p.addline('0. Close')
	p.menuselect = WcssettingsSelectionChangeXp
	p.submenu(8, 'wcscadmin')
	p.submenu(9, 'wcsxpsettings1')

	p = popups['wcsxpsettings1'] = popuplib.create('wcsxpsettings1')
	p.addline('-XP Settings-')
	p.addline(' ')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->1.Raise XP for Planting')
	p.addline('->2.Lower Xp for Planting')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->3.Raise XP for Bomb Explode')
	p.addline('->4.Lower Xp for Bomb Explode')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->5.Raise XP for Defusing')
	p.addline('->6.Lower Xp for Defusing')
	p.addline('-------------------')
	p.addline('->7. Default')
	p.addline('->8. Back')
	p.addline('->9. Next')
	p.addline('0. Close')
	p.menuselect = WcssettingsSelectionChangeXp
	p.submenu(8, 'wcsxpsettings0')
	p.submenu(9, 'wcsxpsettings2')

	p = popups['wcsxpsettings2'] = popuplib.create('wcsxpsettings2')
	p.addline('-XP Settings-')
	p.addline(' ')
	p.addline('-------------------')
	p.addline(' ')
	p.addline('->1.Raise XP per Hostage')
	p.addline('->2.Lower Xp per Hostage')
	p.addline('-------------------')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('-------------------')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('-------------------')
	p.addline('->7. Default')
	p.addline('->8. Back')
	p.addline(' ')
	p.addline('0. Close')
	p.menuselect = WcssettingsSelectionChangeXp
	p.submenu(3, 'wcsxpsettings2')
	p.submenu(4, 'wcsxpsettings2')
	p.submenu(5, 'wcsxpsettings2')
	p.submenu(6, 'wcsxpsettings2')
	p.submenu(7, 'wcsxpsettings2')
	p.submenu(8, 'wcsxpsettings1')
	p.submenu(9, 'wcsxpsettings2')

	p = popups['wcsplayers'] = popuplib.create('wcsplayers')
	p.addline('-WCS Players-')
	p.addline(' ')
	p.addline('->1. Change Players Race')
	p.addline('->2. Player Info')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('->8. Back')
	p.addline(' ')
	p.addline('0. Close')
	p.menuselect = WcsplayersSelection
	for x in xrange(3, 10):
		p.submenu(x, 'wcsplayers')
	p.submenu(8, 'wcscadmin')

	p = popups['wcsadmins'] = popuplib.create('wcsadmins')
	p.addline('-WCSadmins-')
	p.addline(' ')
	p.addline('->1. Add New WCSadmin')
	p.addline('->2. Update WCSadmin')
	p.addline('->3. Delete WCSadmin')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('->8. Back')
	p.addline(' ')
	p.addline('0. Close')
	p.menuselect = WcsadminsSelection
	for x in xrange(4, 10):
		p.submenu(x, 'wcsadmins')
	p.submenu(8, 'wcscadmin')

	p = popups['wcsChelp'] = popuplib.create('wcsChelp')
	p.addline('-WCSmenu-')
	p.addline(' ')
	p.addline('-Races-')
	p.addline('->1. changerace - choose your race')
	p.addline('->2. races - select a race from a list of categories')
	p.addline('->3. raceinfo - show skill info')
	p.addline(' ')
	p.addline('-Skills-')
	p.addline('->4. showxp - shows your xp')
	p.addline('->5. showskills - show all skill levels')
	p.addline('->6. spendskills - spend skill points')
	p.addline('->7. resetskills - resets skills for current race')
	p.addline('->8. spendlevels - spendlevels from the level bank')
	p.addline('->9. Next')
	p.addline('0. Close')
	#p.menuselect = WcsXhelpSelection
	p.submenu(9, 'wcsCpg2')

	p = popups['wcsCpg2'] = popuplib.create('wcsCpg2')
	p.addline('-WCSmenu-')
	p.addline(' ')
	p.addline('-Shop Menu-')
	p.addline('->1. shopmenu - buy shop races')
	p.addline('->2. wcscraces - info about shop races')
	p.addline(' ')
	p.addline('-Info-')
	p.addline('->3. wcs - command for this menu')
	p.addline('->4. wcshelp - more command info')
	p.addline('->5. showtop10 - WCStop 10')
	p.addline('->6. playerinfo - Info about a player')
	p.addline(' ')
	p.addline('->8. Back')
	p.addline('->9. Next')
	p.addline('0. Close')
	#p.menuselect = WcsCrpg2Selection
	p.submenu(7, 'wcsCpg2')
	p.submenu(8, 'wcsChelp')
	p.submenu(9, 'wcsCpg3')

	p = popups['wcsCpg3'] = popuplib.create('wcsCpg3')
	p.addline('-WCSmenu-')
	p.addline(' ')
	p.addline('WCS Admin')
	p.addline('->1. wcsadmin - WCSadmin menu')
	p.addline('->2. wcsCadmin - WCS Custom Admin (Coded by HOLLIDAY)')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline(' ')
	p.addline('->8. Back')
	p.addline(' ')
	p.addline('0. Close')
	#p.menuselect = WcsCrpg3Selection
	for x in xrange(3, 10):
		p.submenu(x, 'wcsCpg3')
	p.submenu(8, 'wcsCpg2')

	cmdlib.registerClientCommand('wcscadmin', register, 'WcsCadmin command')
	cmdlib.registerSayCommand('wcscadmin', register, 'WcsCadmin command')

	if cfgchangerace:
		cmdlib.registerClientCommand('races', register1, 'Races command')
		cmdlib.registerSayCommand('races', register1, 'Races command')
		'''cmdlib.unregisterClientCommand('changerace')
		cmdlib.unregisterSayCommand('changerace')
		cmdlib.registerClientCommand('changerace', register1, 'Changerace command')
		cmdlib.registerSayCommand('changerace', register1, 'Changerace command')'''

def unload():
	for x in popups:
		popuplib.delete(x)

	popups.clear()

	cmdlib.unregisterClientCommand('wcscadmin')
	cmdlib.unregisterSayCommand('wcscadmin')

	if es.exists('saycommand', 'races'):
		cmdlib.unregisterClientCommand('races')
		cmdlib.unregisterSayCommand('races')

	if _doSave:
		wcs.racedb.races.write()
	'''cmdlib.unregisterClientCommand('changerace')
	cmdlib.unregisterSayCommand('changerace')
	if es.exists('script', 'wcs'):
		cmdlib.registerClientCommand('changerace', wcs.changerace.doCommand, 'Changerace command')
		cmdlib.registerSayCommand('changerace', wcs.changerace.doCommand, 'Changerace command')'''

def register(userid, args):
	player = wcs.admin.getPlayer(userid)
	if player.hasFlag('wcscadmin'):
		for x in flags:
			if not x in player:
				player.setFlag(x, 0)

		menu(userid)
	else:
		wcs.tell(userid, 'wcscadmin: not admin')

def menu(userid):
	popups['wcscadmin'].send(userid)

def register1(userid, args):
	doCommand(userid)


#Menu selection
def WcscadminSelection(userid, choice, popupid):
	player = wcs.admin.getPlayer(userid).hasFlag
	if choice == 1:
		if player('wcscadmin_settings'):
			popups['wcssettings'].send(userid)
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

	elif choice == 2:
		if player('wcscadmin_players'):
			popups['wcsplayers'].send(userid)
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

	elif choice == 3:
		if player('wcscadmin_admins'):
			popups['wcsadmins'].send(userid)
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

def XplevelsSelection(userid, choice, popupid):
	pass

def WcssettingsSelection(userid, choice, popupid):
	if choice == 1:
		wcssettingXpSend0(userid)
	elif choice == 2:
		createRaceList(userid, WcsSettingsRaceSettings, backmenu='wcssettings')
	elif choice == 3:
		pass
	elif choice == 4:
		wcsscriptManagement(userid)

def wcssettingXpSend0(userid):
	popups['wcsxpsettings0'].modline(4, '-Kill XP: '+es.ServerVar('wcs_killxp'))
	popups['wcsxpsettings0'].modline(8, '-Head shot: '+es.ServerVar('wcs_headshotxp'))
	popups['wcsxpsettings0'].modline(12, '-Knife Kill: '+es.ServerVar('wcs_knifexp'))
	popups['wcsxpsettings0'].send(userid)

def wcssettingXpSend1(userid):
	popups['wcsxpsettings1'].modline(4, '-Planting: '+str(es.ServerVar('wcs_plantxp')))
	popups['wcsxpsettings1'].modline(8, '-Bomb Explode: '+str(es.ServerVar('wcs_explodexp')))
	popups['wcsxpsettings1'].modline(12, '-Defusing: '+str(es.ServerVar('wcs_defusexp')))
	popups['wcsxpsettings1'].send(userid)

def wcssettingXpSend2(userid):
	popups['wcsxpsettings2'].modline(4, '-Hostage: '+str(es.ServerVar('wcs_hostagexp')))
	popups['wcsxpsettings2'].send(userid)

_xpSend = {'wcsxpsettings0':wcssettingXpSend0,
		   'wcsxpsettings1':wcssettingXpSend1,
		   'wcsxpsettings2':wcssettingXpSend2}

_xpChange = {'wcsxpsettings0':{'wcs_killxp':30,'wcs_headshotxp':15,'wcs_knifexp':40},
			 'wcsxpsettings1':{'wcs_plantxp':15,'wcs_explodexp':15,'wcs_defusexp':30},
			 'wcsxpsettings2':{'wcs_hostagexp':10}}

_xpValues = {'wcsxpsettings0':{1:('wcs_killxp','+'),2:('wcs_killxp','-'),3:('wcs_headshotxp','+'),4:('wcs_headshotxp','-'),5:('wcs_knifexp','+'),6:('wcs_knifexp','-')},
			 'wcsxpsettings1':{1:('wcs_plantxp','+'),2:('wcs_plantxp','-'),3:('wcs_explodexp','+'),4:('wcs_explodexp','-'),5:('wcs_defusexp','+'),6:('wcs_defusexp','-')},
			 'wcsxpsettings2':{1:('wcs_hostagexp','+'),2:('wcs_hostagexp','-')}}

_xpConvert = {'wcsxpsettings0':{8:'wcssettings',9:'wcsxpsettings1'},
			  'wcsxpsettings1':{8:'wcsxpsettings0',9:'wcsxpsettings2'},
			  'wcsxpsettings2':{8:'wcsxpsettings1',9:'wcsxpsettings2'}}

def WcssettingsSelectionChangeXp(userid, choice, popupid):
	if choice in xrange(1, 7):
		var = es.ServerVar(_xpValues[popupid][choice][0])
		value = int(var)
		do = _xpValues[popupid][choice][1]

		if do == '+':
			var.set(value+5)
			_xpSend[popupid](userid)
			#popups[popupid].send(userid)
		elif do == '-':
			if value-5 < 0:
				es.tell(userid, 'Unable to set value to lessthan 0')
				_xpSend[popupid](userid)
			else:
				var.set(value-5)
				_xpSend[popupid](userid)
				#popups[popupid].send(userid)

	elif choice == 7:
		for i, v in _xpChange[popupid].iteritems():
			es.ServerVar(i).set(v)

		_xpSend[popupid](userid)

	elif choice in (8,9):
		v = _xpConvert[popupid][choice]
		if v.startswith('wcsxpsettings'):
			_xpSend[v](userid)
		else:
			popups[v].send(userid)

def WcsSettingsRaceSettings(userid, choice, popupid):
	WcsSettingSendRaceSettings(userid, choice)

_tmp = {}
def WcsSettingSendRaceSettings(userid, race):
	global _tmp
	_tmp[int(userid)] = race
	raceinfo = wcs.racedb.getRace(race)
	p = popups['_wcsracemenuinfo'] = popuplib.create('_wcsracemenuinfo')
	p.addline(race)
	p.addline('-Author: '+str(raceinfo['author']))
	p.addline('______________________')
	p.addline('-Maximum Level '+str(raceinfo['maximum']))
	p.addline('-Required Level '+str(raceinfo['required']))
	#p.addline('-Team Limit '+str(raceinfo['teamlimit']))

	try:
		p.addline('-Team Limit '+str(raceinfo['teamlimit']))
	except KeyError:
		p.addline('-Team Limit ERROR')
		logging.log('wcsCadmin: Error: A race ('+race+') is missing the teamlimit key')

	if 'player_ultimate' in raceinfo['skillcfg']:
		cooldown = str(raceinfo['skill'+str(raceinfo['skillcfg'].split('|').index('player_ultimate')+1)]['cooldown'])
	else:
		cooldown = 'n/a'
	p.addline('-Ultimate Cooldown '+cooldown)
	p.addline('-----------------------------')
	p.addline('->1. Raise Maximum Level +')
	p.addline('->2. Lower Maximum Level -')
	p.addline('->3. Raise Required Level +')
	p.addline('->4. Lower Required Level -')
	p.addline('->5. Change Team Limit (1-10)')
	p.addline('->6. Raise ultimate_cooldown +')
	p.addline('->7. Lower ultimate_cooldown -')
	p.addline('->8. Back')
	p.addline(' ')
	p.addline('0. Close')

	p.menuselect = WcsSettingsRaceSettingsSelection

	p.send(userid)

_doSave = False
def WcsSettingsRaceSettingsSelection(userid, choice, popupid):
	race = _tmp[int(userid)]
	raceinfo = wcs.racedb.getRace(race)
	if choice in xrange(1, 8):
		global _doSave
		if choice == 1:
			v = int(raceinfo['maximum'])
			raceinfo['maximum'] = v + 1
			_doSave = True

		elif choice == 2:
			v = int(raceinfo['maximum'])
			if v == 0:
				es.tell(userid, 'Unable to set value to lessthan 0')
			else:
				raceinfo['maximum'] = v - 1
				_doSave = True

		elif choice == 3:
			v = int(raceinfo['required'])
			raceinfo['required'] = v + 1
			_doSave = True

		elif choice == 4:
			v = int(raceinfo['required'])
			if v == 0:
				es.tell(userid, 'Unable to set value to lessthan 0')
			else:
				raceinfo['required'] = v - 1
				_doSave = True

		elif choice == 5:
			try:
				v = int(raceinfo['teamlimit'])
				raceinfo['teamlimit'] = v + 1
				if v == 10:
					raceinfo['teamlimit'] = 0

				_doSave = True
			except KeyError:
				logging.log('wcsCadmin: Error: A race ('+race+') is missing the team limit key')

		elif choice == 6:
			info = raceinfo['skillcfg'].split('|')
			if 'player_ultimate' in info:
				index = info.index('player_ultimate')
				skill = 'skill'+str(index+1)
				v = str(raceinfo[skill]['cooldown']).split('|')
				if not len(v) == 1:
					es.tell(userid, 'Unable to change cooldown on multiple objects')
				else:
					v = int(v[0])
					raceinfo[skill]['cooldown'] = v + 1
					_doSave = True
			else:
				es.tell(userid, 'No ultimate was found.')

		elif choice == 7:
			info = raceinfo['skillcfg'].split('|')
			if 'player_ultimate' in info:
				index = info.index('player_ultimate')
				skill = 'skill'+str(index+1)
				v = str(raceinfo[skill]['cooldown']).split('|')
				if not len(v) == 1:
					es.tell(userid, 'Unable to change cooldown on multiple objects')
				else:
					v = int(v[0])
					if v == 0:
						es.tell(userid, 'Unable to set value to lessthan 0')
					else:
						raceinfo[skill]['cooldown'] = v - 1
						_doSave = True
			else:
				es.tell(userid, 'No ultimate was found.')

		WcsSettingSendRaceSettings(userid, race)

	elif choice == 8:
		createRaceList(userid, WcsSettingsRaceSettings, backmenu='wcssettings')




def WcsplayersSelection(userid, choice, popupid):
	player = wcs.admin.getPlayer(userid)

	if choice == 1:
		if player.hasFlag('wcscadmin_force_changerace'):
			createPlayerList(userid, ForceChangeRace)
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

	elif choice == 2:
		if player.hasFlag('wcscadmin_playerinfo'):
			createPlayerList(userid, PlayerInfo)
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

def ForceChangeRace(userid, choice, popupid):
	pass

def PlayerInfo(userid, choice, popupid):
	pass

def WcsadminsSelection(userid, choice, popupid):
	player = wcs.admin.getPlayer(userid)
	if choice == 1:
		if player.hasFlag('wcscadmin_add_new_admin'):
			createPlayerList(userid, addNewAdmins, '-Add a New WCSadmin-', '#human', backmenu='wcsadmins', check=lambda x: not wcs.admin.getPlayer(x).hasFlag('wcscadmin'))
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

	elif choice == 2:
		if player.hasFlag('wcscadmin_update_admin'):
			createPlayerList(userid, editAdmins, tag='#human', backmenu='wcsadmins', check=lambda x: wcs.admin.getPlayer(x).hasFlag('wcscadmin'))
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

	elif choice == 3:
		if player.hasFlag('wcscadmin_delete_admin'):
			createPlayerList(userid, deleteAdmins, 'Delete a WCSadmin', '#human', backmenu='wcsadmins', check=lambda x: wcs.admin.getPlayer(x).hasFlag('wcscadmin'))
		else:
			popups[popupid].send(userid)
			wcs.tell(userid, 'wcscadmin: not access')

def addNewAdmins(userid, choice, popupid):
	if es.exists('userid', choice):
		wcs.admin.getPlayer(choice).setFlag('wcscadmin')
		wcs.logging.log('wcsadmin: Information: '+es.getplayername(userid)+' ('+es.getplayersteamid(userid)+') added '+es.getplayername(choice)+' ('+es.getplayersteamid(choice)+') as an WcsCAdmin')
	else:
		createPlayerList(userid, addNewAdmins, '-Add a New WCSadmin-', '#human', backmenu='wcsadmins', check=lambda x: not wcs.admin.getPlayer(x).hasFlag('wcscadmin'))

def editAdmins(userid, choice, popupid):
	if es.exists('userid', choice):
		changeFlag(userid, choice)
	else:
		createPlayerList(userid, editAdmins, tag='#human', backmenu='wcsadmins', check=lambda x: wcs.admin.getPlayer(x).hasFlag('wcscadmin'))
		wcs.tell(userid, 'wcscadmin: unknown player')

def changeFlag(userid, target):
	pname = 'wcscoption_'+str(userid)+'_'+str(target)
	convert = lambda x: ['Off', 'On'][int(bool(wcs.admin.getPlayer(target).hasFlag(x)))]
	p = popups[pname] = popuplib.create(pname)
	p.addline('-WCSadmin Flags-')
	p.addline(' ')
	p.addline('->1. Set all flags')
	p.addline('->2. Remove all flags')
	p.addline('->3. Admin Settings: '+str(convert('wcscadmin_update_admin')))
	p.addline('->4. Force changerace: '+str(convert('wcscadmin_force_changerace')))
	p.addline('->5. Give Money: '+str(convert('wcscadmin_give_cash')))
	p.addline('->6. Give Players Xp/Levels: '+str(convert('wcscadmin_give_players')))
	p.addline('->7. Give Self Xp/Levels: '+str(convert('wcscadmin_give_self')))
	p.addline('->8. Back')
	p.addline(' ')
	#p.addline('->9. Next')
	p.addline('0. Close')
	p.menuselect = changeFlagSelection
	p.send(userid)

def changeFlagSelection(userid, choice, popupid):
	target = popupid.split('_')[2]

	if es.exists('userid', target):
		player = wcs.admin.getPlayer(target)
		convert = lambda x: int(bool(player.hasFlag(x)))
		if choice == 1:
			for x in flags:
				player.setFlag(x)
			changeFlag(userid, target)

		elif choice == 2:
			for x in flags:
				player.setFlag(x, 0)
			changeFlag(userid, target)

		elif choice == 3:
			player.setFlag('wcscadmin_update_admin', int(not player.getFlag('wcscadmin_update_admin')))
			changeFlag(userid, target)

		elif choice == 4:
			player.setFlag('wcscadmin_force_changerace', int(not player.getFlag('wcscadmin_force_changerace')))
			changeFlag(userid, target)

		elif choice == 5:
			player.setFlag('wcscadmin_give_cash', int(not player.getFlag('wcscadmin_give_cash')))
			changeFlag(userid, target)

		elif choice == 6:
			player.setFlag('wcscadmin_give_players', int(not player.getFlag('wcscadmin_give_players')))
			changeFlag(userid, target)

		elif choice == 7:
			player.setFlag('wcscadmin_give_self', int(not player.getFlag('wcscadmin_give_self')))
			changeFlag(userid, target)

		elif choice == 8:
			createPlayerList(userid, editAdmins, tag='#human', backmenu='wcsadmins', check=lambda x: wcs.admin.getPlayer(x).hasFlag('wcscadmin'))

		elif choice == 9:
			return
			changeFlag1(userid, target)
	else:
		createPlayerList(userid, editAdmins, tag='#human', backmenu='wcsadmins', check=lambda x: wcs.admin.getPlayer(x).hasFlag('wcscadmin'))
		wcs.tell(userid, 'wcscadmin: unknown player')

def deleteAdmins(userid, choice, popupid):
	if es.exists('userid', choice):
		wcs.admin.getPlayer(choice).setFlag('wcscadmin', 0)
		wcs.logging.log('wcsadmin: Information: '+es.getplayername(userid)+' ('+es.getplayersteamid(userid)+') removed '+es.getplayername(choice)+' ('+es.getplayersteamid(choice)+') as an WcsCAdmin')
	else:
		createPlayerList(userid, deleteAdmins, 'Delete a WCSadmin', '#human', backmenu='wcsadmins', check=lambda x: wcs.admin.getPlayer(x).hasFlag('wcscadmin'))
		wcs.tell(userid, 'wcscadmin: unknown player')




#Functions
def createPlayerList(userid, callback, title='Select a player', tag='#all', popupname='_wcsplayerlist', backmenu=None, check=None):
	p = popuplib.easymenu(popupname, '_popup_choice', callback)
	p.settitle(title)

	p.c_beginsep = None
	p.c_pagesep = None

	players = playerlib.getPlayerList(tag)

	if not check is None:
		players = filter(check, players)

	for user in players:
		p.addoption(user.userid, user.name)

	if not backmenu is None:
		p.submenu(10, backmenu)
		p.c_exitformat = '0. Back'

	p.send(userid)

def createRaceList(userid, callback, title='Please choose a race', popupname='_wcsracelist', backmenu=None, check=None):
	if popupname in popups:
		popups[popupname].send(userid)
		return

	p = popups[popupname] = popuplib.easymenu(popupname, '_popup_choice', callback)
	p.settitle(title)

	p.c_beginsep = None
	p.c_pagesep = None

	races = wcs.racedb.getAll()

	if not check is None:
		races = filter(check, races)

	for race in races:
		p.addoption(race, race)

	if not backmenu is None:
		p.submenu(10, backmenu)
		p.c_exitformat = '0. Back'

	p.send(userid)

def doCommand(userid, args='race7', tell=True):
	if args == 'race':
		args = 'race7'

	positionsearch = str(args.replace('wcscraces', '').strip())

	if len(positionsearch):
		if positionsearch.isdigit():
			positionsearch = int(positionsearch)
		else:
			positionsearch = 7
	else:
		positionsearch = 7

	allraces = racedb.keys()

	del allraces[:positionsearch - 7]
	del allraces[positionsearch:]

	if len(allraces):
		pname = 'wcscraces_%s_%s'%(userid, positionsearch)

		wcscraces = popuplib.create(pname)

		wcscraces.addline('Choose a category')

		wcscraces.addline(' ')
		wcscraces.menuselect = popupHandler

		added = 0
		for race in allraces:
			if added < 7:
				added += 1
				wcscraces.addline('->'+str(added)+'. '+race)
			else:
				break

		while added < 8:
			wcscraces.addline(' ')
			added += 1
			wcscraces.submenu(added, pname)

		wcscraces.addline(' ')
		if positionsearch < 8:
			wcscraces.addline(' ')
			wcscraces.submenu(8, pname)
		else:
			wcscraces.addline('->8. Back')

		if len(allraces) < positionsearch:
			wcscraces.addline(' ')
			wcscraces.submenu(9, pname)
		else:
			wcscraces.addline('->9. Next')

		wcscraces.addline('0. Close')

		wcscraces.send(userid)

def popupHandler(userid, choice, popupid):
	last_split  = popupid.split('_')
	last_search = int(last_split[2])

	if choice == 8:
		if last_search < 0:
			doCommand(userid, 'wcscraces7')

		elif last_search < 6:
			send(popupid, userid)

		else:
			newsearch = int(last_search)-7
			doCommand(userid, 'wcscraces%s'%newsearch)

	elif choice == 9:
		if last_search >= len(wcs.wcs.itemdb.getSections()):
			send(popupid, userid)

		else:
			newsearch = int(last_search)+7
			doCommand(userid, 'wcscraces%s'%newsearch)

	elif choice < 8:
		#popup = 'wcscraces_%s_%s_7'%(userid, divmod(last_search, 7)[0]*7-(8-choice))
		popup = 'wcscraces_%s_%s_7'%(userid, choice)
		doCommand1(userid, popup)

def doCommand1(userid, args):
	try:
		args = args.split('_')
		choice = int(args[2])
		last_search = int(args[3])
		shop_select = choice-1

		itemkeys = racedb.keys()

		values = itemkeys[shop_select]
		allvalues = racedb.get(values)
		#allvalues = list(values)

		del allvalues[:last_search - 7]
		del allvalues[last_search:]

		pname = 'wcscraces_%s_%s_%s'%(userid, choice, last_search)

		wcscraces = popuplib.create(pname)

		added = 0
		totallevel = wcs.getPlayer(userid).player.totallevel
		for race in allvalues:
			if added < 7:
				added += 1
				raceinfo = wcs.racedb.getRace(race)

				if not wcs.curmap in raceinfo['restrictmap'].split('|'):
					admins = raceinfo['allowonly'].split('|')
					if len(admins) == 1 and not admins[0]:
						del admins[0]

					if not len(admins) or len(admins) and es.getplayersteamid(userid) in admins or 'ADMINS' in admins and es.getplayersteamid(userid) in wcs.admin.admins:
						team = int(es.getplayerteam(userid))
						if not raceinfo['restrictteam'] or not int(raceinfo['restrictteam']) == team:
							if totallevel >= int(raceinfo['required']):
								if int(raceinfo['maximum']) and totallevel <= int(raceinfo['maximum']):
									wcscraces.addline(str(added)+'. '+str(race)+' (maximum level '+str(raceinfo['maximum'])+')')
									wcscraces.submenu(added, pname)
								else:
									wcscraces.addline('->'+str(added)+'. '+str(race))
							else:
								wcscraces.addline(str(added)+'. '+str(race)+' (minimum level '+raceinfo['required']+')')
								wcscraces.submenu(added, pname)
						else:
							wcscraces.addline(str(added)+'. '+str(race)+' (restricted team '+{2:'T',3:'CT'}[team]+')')
							wcscraces.submenu(added, pname)
					else:
						wcscraces.addline(str(added)+'. '+str(race)+' (private race)')
						wcscraces.submenu(added, pname)
				else:
					wcscraces.addline(str(added)+'. '+str(race)+' (restricted map '+wcs.curmap+')')
					wcscraces.submenu(added, pname)
			else:
				break

		while added < 8:
			wcscraces.addline(' ')
			added += 1
			wcscraces.submenu(added, pname)

		wcscraces.menuselect = popupHandler1

		wcscraces.addline(' ')
		wcscraces.addline('->8. Back')

		if len(allvalues) <= last_search+1:
			wcscraces.addline(' ')
			wcscraces.submenu(9, pname)
		else:
			wcscraces.addline('->9. Next')

		wcscraces.addline('0. Close')

		wcscraces.send(userid)
	except IndexError:
		pass

def popupHandler1(userid, choice, popupid):
	userid = int(userid)
	last_split  = popupid.split('_')
	test = int(last_split[2])
	last_search = int(last_split[3])

	if choice <= 7:
		itemkeys = racedb.keys()

		values = itemkeys[test-1]
		allraces = racedb.get(values)

		#del allraces[:last_search - 7]
		#del allraces[last_search:]

		player = wcs.getPlayer(userid)
		totallevel = player.player.totallevel

		race = allraces[divmod(last_search, 7)[0]*7-(8-choice)]
		raceinfo = wcs.racedb.getRace(race)
		team = int(es.getplayerteam(userid))
		admins = raceinfo['allowonly'].split('|')
		if len(admins) == 1 and not admins[0]:
			del admins[0]

		if wcs.curmap in raceinfo['restrictmap'].split('|'):
			wcs.tell(userid, 'changerace: restricted map', {'race':race, 'map':wcs.curmap})

		elif len(admins) and es.getplayersteamid(userid) not in admins or 'ADMINS' in admins and not es.getplayersteamid(userid) in wcs.admin.admins:
			wcs.tell(userid, 'changerace: restricted map', {'race':race, 'map':wcs.curmap})

		elif raceinfo['restrictteam'] and int(raceinfo['restrictteam']) == team:
			wcs.tell(userid, 'changerace: restricted team', {'race':race, 'team':{2:'T',3:'CT'}[team]})

		elif totallevel < int(raceinfo['required']):
			diffience = str(int(raceinfo['required'])-int(player.player.totallevel))
			wcs.tell(userid, 'changerace: required level', {'race':race, 'diffience':diffience})

		elif int(raceinfo['maximum']) and totallevel > int(raceinfo['maximum']):
			diffience = str(int(player.player.totallevel)-int(raceinfo['maximum']))
			wcs.tell(userid, 'changerace: high level', {'race':race, 'diffience':diffience})

		else:
			wcs.tell(userid, 'changerace: change race', {'race':race})
			player.changeRace(race)

			es.keydelete('WCSuserdata', userid)
			es.keycreate('WCSuserdata', userid)
			wcs.wcsgroup.delUser(userid)
			wcs.wcsgroup.addUser(userid)

	elif choice == 8:
		if last_search <= 0:
			doCommand(userid)

		elif last_search < 7:
			doCommand(userid, 'wcscraces'+str(last_search))

		else:
			newsearch = int(last_search)-1
			doCommand1(userid, 'wcscraces_%s_%s_%s'%(userid, test, newsearch))

	elif choice == 9:
		if last_search >= len(item):
			send(popupid, userid)

		else:
			newsearch = int(last_search)+1
			doCommand1(userid, 'wcscraces_%s_%s_%s'%(userid, test, newsearch))








