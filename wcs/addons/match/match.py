import es
import cmdlib
from wcs import wcs


playerDict = {}

def load():
	if es.exists('saycommand', 'changerace'):
		cmdlib.unregisterSayCommand('changerace')
		cmdlib.unregisterClientCommand('changerace')
	if es.exists('saycommand', 'wcs'):
		cmdlib.unregisterSayCommand('wcs')
		cmdlib.unregisterClientCommand('wcs')
		cmdlib.unregisterSayCommand('wcsmenu')
		cmdlib.unregisterClientCommand('wcsmenu')
		cmdlib.unregisterSayCommand('wcshelp')
		cmdlib.unregisterClientCommand('wcshelp')

	cmdlib.registerSayCommand('changerace',    changeraceRegister, '')
	cmdlib.registerClientCommand('changerace', changeraceRegister, '')

	cmdlib.registerSayCommand('wcs',           disabled, '')
	cmdlib.registerClientCommand('wcs',        disabled, '')
	cmdlib.registerSayCommand('wcsmenu',       disabled, '')
	cmdlib.registerClientCommand('wcsmenu',    disabled, '')
	cmdlib.registerSayCommand('wcshelp',       disabled, '')
	cmdlib.registerClientCommand('wcshelp',    disabled, '')

	#wcs.changerace.callBack = tmpChangeraceHolder

def unload():
	cmdlib.unregisterSayCommand('changerace')
	cmdlib.unregisterClientCommand('changerace')

	cmdlib.unregisterSayCommand('wcs')
	cmdlib.unregisterClientCommand('wcs')
	cmdlib.unregisterSayCommand('wcsmenu')
	cmdlib.unregisterClientCommand('wcsmenu')
	cmdlib.unregisterSayCommand('wcshelp')
	cmdlib.unregisterClientCommand('wcshelp')

	#Register them back to their rightfull place
	cmdlib.registerSayCommand('changerace',    wcs.cmdreg.changerace, '')
	cmdlib.registerClientCommand('changerace', wcs.cmdreg.changerace, '')

	cmdlib.registerSayCommand('wcs',           wcs.cmdreg.wcsmenu,    '')
	cmdlib.registerClientCommand('wcs',        wcs.cmdreg.wcsmenu,    '')
	cmdlib.registerSayCommand('wcsmenu',       wcs.cmdreg.wcsmenu,    '')
	cmdlib.registerClientCommand('wcsmenu',    wcs.cmdreg.wcsmenu,    '')
	cmdlib.registerSayCommand('wcshelp',       wcs.cmdreg.wcsmenu,    '')
	cmdlib.registerClientCommand('wcshelp',    wcs.cmdreg.wcsmenu,    '')

	#wcs.changerace.callBack = wcs.changerace.popupHandler

def disabled(userid, args):
	wcs.tell(userid, 'match: disabled')

def changeraceRegister(userid, args):
	steamid = str(es.getplayersteamid(userid))
	player_activate({'es_steamid':steamid})

	if playerDict[steamid]['race'] > 0:
		tmpdoCommand(userid)
	else:
		wcs.tell(userid, 'match: maximum changerace')

def tmpdoCommand(userid):
	if not popuplib.exists('tmp_changerace'):
		popup = popuplib.create('tmp_changerace')

		popup.menuselect = tmppopupHandler

		popup.addline('WCS Tournament')
		popup.addline('Changerace Menu')
		popup.addline(' ')
		popup.addline('->1. Undead Scourge')
		popup.addline('->2. Human Alliance')
		popup.addline('->3. Orcish Horde')
		popup.addline('->4. Night Elves')
		popup.addline('->5. Blood Mage')
		popup.addline('->6. Archmage Proudmoore')
		popup.addline('->7. Warden')
		popup.addline('->8. Crypt Lord')
		popup.addline(' ')
		popup.addline('0. Close')

	popuplib.send('tmp_changerace', userid)

raceChoice = {1:'Undead Scourge',
			  2:'Human Alliance',
			  3:'Orcish Horde',
			  4:'Night Elves',
			  5:'Blood Mage',
			  6:'Archmage Proudmoore',
			  7:'Warden',
			  8:'Crypt Lord'}

def tmppopupHandler(userid, choice, popupid):
	if choice < 9:
		player = wcs.getPlayer(userid)
		player.changeRace(raceChoice[choice])
		wcs.tell(userid, 'match: changerace', {'race':raceChoice[choice]})

		race = wcs.racedb.getRace(raceChoice[choice])
		skills = race['numberofskills']
		levels = race['numberoflevels']

		skillinfo = []
		while len(skillinfo) < skills:
			skillinfo.append(str(levels))

		player.race.skills = '|'.join(skillinfo)

		wcs.tell(userid, 'match: maxed')



#EVENTS
def player_activate(ev):
	steamid = str(ev['es_steamid'])
	if not steamid in playerDict:
		global playerDict
		playerDict[steamid] = {'race':3}

def player_spawn(ev):
	pass

def es_map_start(ev):
	playerDict.clear()
