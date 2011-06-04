import es, popuplib, playerlib, gamethread, usermsg, cfglib, cmdlib, langlib, saytextlib, os, random, time, sys, psyco, logging, core

psyco.full()
from path import path as Path
from sqlite3 import dbapi2 as sqlite
from base64 import encodestring as estr, decodestring as dstr
from configobj import ConfigObj

reload(logging)
reload(core)

from core import *


version = 'v0.78.5g.4d Beta'
author = '['+version+' by kRypT0n!Te & Tha Pwned]'
game = es.getGameName()
ragdoll = {'cstrike':'cs_ragdoll', 'hl2dm':'hl2dm_ragdoll', 'tf':'tf_ragdoll', 'dod':'dod_ragdoll'}.get(game)


class InI(object):
	def __init__(self):
		self.path = es.getAddonPath('wcs')

		self.races = os.path.join(self.path, 'ini', 'races.ini')
		self._races = os.path.join(self.path, 'ini', '_backupraces.ini')
		self.items = os.path.join(self.path, 'ini', 'items.ini')

	@property
	def getRaces(self):
		try:
			return ConfigObj(self.races)
		except:
			sys.excepthook(*sys.exc_info())
			logging.log('wcs: Error: Unable to load races.ini, there was an error')
			logging.log('wcs: Information: Loading the backup races...')
			return ConfigObj(self._races)

	@property
	def getItems(self):
		return ConfigObj(self.items)
ini = InI()

if os.path.isfile(os.path.join(ini.path, 'ini', 'strings.ini')):
	strings = langlib.Strings(os.path.join(ini.path, 'ini', 'strings.ini'))
else:
	logging.log('wcs: Error: Unable to load the strings.ini located in wcs/ini/')
	strings = lambda x, tokens={}, lang='en': logging.log('wcs: Error: Can\'t find strings.ini inside wcs/ini/')

config = cfglib.AddonCFG(os.path.join(ini.path, 'config', 'config.cfg'))

log						= config.cvar('wcs_log',					0,  'Will log specific events (-1 = OFF, 0 = ONLY SHOWS ERRORS, GREATERTHAN 0 = OTHERS)')

interval				= config.cvar('wcs_cfg_interval',				80, 'XP required for level up (LEVEL * interval)')
bonusxp					= config.cvar('wcs_cfg_bonusxp',				4,  'Extra XP gained per level diffience (LEVEL * bonusxp) when killing a higher level enemy')
killxp					= config.cvar('wcs_cfg_killxp',					30, 'XP gained per kill')
knifexp					= config.cvar('wcs_cfg_knifexp',				40, 'XP gained for a knife kill')
headshotxp				= config.cvar('wcs_cfg_headshotxp',				15, 'XP gained for making a headshot')

allow_player_hurt		= config.cvar('wcs_cfg_allow_player_hurt',		1,  'Allow the player_hurt event for races and items (1 = ON, 0 = OFF)')
allow_player_spawn		= config.cvar('wcs_cfg_allow_player_spawn',		1,  'Allow the player_spawn event for races and items (1 = ON, 0 = OFF)')
allow_player_death		= config.cvar('wcs_cfg_allow_player_death',		1,  'Allow the player_death event for races and items (1 = ON, 0 = OFF)')
allow_player_kill		= config.cvar('wcs_cfg_allow_player_kill',		1,  'Allow the player_kill event for races and items (1 = ON, 0 = OFF)')
allow_player_attacker	= config.cvar('wcs_cfg_allow_player_attacker',	1,  'Allow the player_attacker event for races and items (1 = ON, 0 = OFF)')
allow_player_victim		= config.cvar('wcs_cfg_allow_player_victim',	1,  'Allow the player_victim event for races and items (1 = ON, 0 = OFF)')
allow_player_say		= config.cvar('wcs_cfg_allow_player_say',		1,  'Allow the player_say event for races and items (1 = ON, 0 = OFF)')

welcometext				= config.cvar('wcs_cfg_welcometext',			1,  'Welcome text (0 = OFF, 1 = ON), delay of 10 seconds')
welcomeguitext			= config.cvar('wcs_cfg_welcomeguitext',			1,  'Welcome gui text (0 = OFF, 1 = ON), delay of 5 seconds')
spawntext				= config.cvar('wcs_cfg_spawntext',				1,  'Spawn text, showed up every round. Good for new servers with WCS beginners (0 = OFF, 1 = ON)')
disabletextonlvl		= config.cvar('wcs_cfg_disabletextonlvl',		20, 'If a player reaches this level, no welcome/gui/spawn text will appear')
graphicfx				= config.cvar('wcs_cfg_graphicfx',				1,  'Show vissual effect (0 = OFF, 1 = ON)')
friendlyexplosion		= config.cvar('wcs_cfg_friendlyexplosion',		0,  'Set this to 1 if you want explode effects (e.g. Suicide Bomber) to inflict friendly players in range')
xpsaver					= config.cvar('wcs_cfg_savexponround',			5,  'The numbers of rounds before the xp/levels are saved (set to 0 to disable)')
showracelevel			= config.cvar('wcs_cfg_showracelevel',			1,  'Show level on changerace (0 = OFF, 1 = ON)')
removeragdolls			= config.cvar('wcs_cfg_removeragdolls',			0,  'Removes ragdolls from the game (0 = OFF, 1 = ON)')
allowshopmenu			= config.cvar('wcs_cfg_enableshopmenu',			1,  'Shopmenu (0 = OFF, 1 = ON)')
allowbotsgetxp			= config.cvar('wcs_cfg_allowbotsgetxp',			1,  'Allow bots getting XP (0 = OFF, 1 = ON)')
allowbotsreward			= config.cvar('wcs_cfg_allowbotsreward',		1,  'Allow players getting XP by killing bots (0 = OFF, 1 = ON)')

config.write()

cfgdata = {'interval':				interval,
		   'bonusxp':				bonusxp,
		   'killxp':				killxp,
		   'knifexp':				knifexp,
		   'headshotxp':			headshotxp,
		   'allow_player_hurt':		allow_player_hurt,
		   'allow_player_spawn':	allow_player_spawn,
		   'allow_player_death':	allow_player_death,
		   'allow_player_kill':		allow_player_kill,
		   'allow_player_attacker':	allow_player_attacker,
		   'allow_player_victim':	allow_player_victim,
		   'allow_player_say':		allow_player_say}

class itemDatabase(object):
	def __init__(self):
		self.items = ini.getItems
		self.sectionlist = []
		self.itemlist = []
		self.itemtosection = {}

		for section in self.items:
			self.sectionlist.append(section)
			for item in self.items[section]:
				if item == 'desc':
					continue

				self.itemlist.append(item)
				self.itemtosection[item] = section

	def __contains__(self, item):
		return item in self.items

	def __iter__(self):
		for x in self.items:
			yield x

	def __getitem__(self, item):
		return self.items[item]

	def keys(self):
		return self.items.keys()

	def getSection(self, section):
		return dict(self.items[section])

	def getItem(self, item):
		return dict(self.items[self.getSectionFromItem(item)][item])

	def getSections(self):
		return list(self.sectionlist)

	def getItems(self):
		return list(self.itemlist)

	def getSectionFromItem(self, item):
		if item in self.itemtosection:
			return self.itemtosection[item]

		return None

	def getAll(self):
		return dict(self.items)
itemdb = itemDatabase()

class raceDatabase(object):
	def __init__(self):
		self.races = ini.getRaces

	def __contains__(self, race):
		return race in self.races

	def __iter__(self):
		for x in self.races:
			yield x

	def getRace(self, race):
		return self.races[race]

	def getAll(self):
		return self.races

	def getAlias(self):
		return aliass

	def index(self, race):
		return self.races.keys().index(race)
racedb = raceDatabase()

if len(racedb.getAll()):
	standardrace = racedb.getAll().keys()[0]
else:
	logging.log('No races found in ini/races.ini')
	raise NotImplementedError
info = es.AddonInfo()




info.author = author

#Thanks to Freddukes for this!
class SQLiteManager(object):
	def __init__(self, pathFile):
		if isinstance(pathFile, Path):
			self.pathFile = pathFile
		else:
			self.pathFile = Path(pathFile)

		self.connection   = sqlite.connect(self.pathFile.joinpath('players.sqlite'))
		self.cursor       = self.connection.cursor()

		self.connection.text_factory = str
		self.execute("PRAGMA synchronous=OFF")
		#self.execute("PRAGMA journal_mode=OFF")
		self.execute("PRAGMA locking_mode=EXCLUSIVE")

		self.execute("""\
			CREATE TABLE IF NOT EXISTS Players (
				UserID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				steamid       VARCHAR(30) NOT NULL,
				currace       VARCHAR(30) NOT NULL,
				name          VARCHAR(30) NOT NULL,
				totallevel    INTEGER DEFAULT 0,
				lastconnect   INTEGER
			)""")

		self.execute("CREATE INDEX IF NOT EXISTS playersIndex ON Players(steamid)")

		self.execute("""\
			CREATE TABLE IF NOT EXISTS Races (
				RaceID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				UserID        INTEGER NOT NULL,
				name          VARCHAR(50) NOT NULL,
				skills        VARCHAR(50) NOT NULL,
				level         INTEGER DEFAULT 0,
				xp            INTEGER DEFAULT 0,
				unused        INTEGER DEFAULT 0
			)""")

		self.execute("CREATE INDEX IF NOT EXISTS racesIndex ON Races(UserID)")

	def __len__(self):
		self.execute("SELECT COUNT(*) FROM Players")
		return int(self.cursor.fetchone()[0])

	def __contains__(self, user):
		if isinstance(user, int):
			self.execute("SELECT steamid FROM Players WHERE UserID = ?", (user, ))
		else:
			self.execute("SELECT steamid FROM Players WHERE steamid = ?", (user, ))
		return bool(self.cursor.fetchone())

	def __del__(self):
		self.save()
		self.close()

	def execute(self, statement, args=None):
		if args is None:
			self.cursor.execute(statement)
		else:
			self.cursor.execute(statement, args)

	def fetchone(self):
		result = self.cursor.fetchone()
		if hasattr(result, '__iter__'):
			if len(result) == 1:
				return result[0]
		return result   

	def fetchall(self):
		trueValues = []
		for value in self.cursor.fetchall():
			if isinstance(value, tuple):
				if len(value) > 1:
					trueValues.append(value)
				else:
					trueValues.append(value[0])
			else:
				trueValues.append(value)
		return trueValues

	def save(self):
		self.connection.commit()

	def close(self):
		self.cursor.close()
		self.connection.close()

	def getUserIdFromSteamId(self, steamid):
		self.execute("SELECT UserID FROM Players WHERE steamid = ?", (steamid, ))
		value = self.cursor.fetchone()
		if value is None:
			return None

		return value[0]

	def addPlayer(self, steamid, name):
		self.execute("INSERT OR IGNORE INTO Players (steamid, currace, name, totallevel, lastconnect) VALUES (?,?,?,0,?)", (steamid, standardrace, self.removeWarnings(name), time.time()))
		return self.cursor.lastrowid

	def getRaceIdFromUserIdAndRace(self, userid, race):
		if not isinstance(userid, int):
			userid = self.getUserIdFromSteamId(userid)

		self.execute("SELECT RaceID FROM Races WHERE UserID = ? AND name = ?", (userid, race))
		value = self.cursor.fetchone()
		if value is None:
			return None

		return value[0]

	def addRaceIntoPlayer(self, userid, name):
		if not isinstance(userid, int):
			userid = self.getUserIdFromSteamId(userid)

		self.execute("INSERT OR IGNORE INTO Races (UserID, name, skills) VALUES (?,?,'')", (userid, name))
		return self.cursor.lastrowid

	def updateRank(self):
		self.execute("SELECT steamid FROM Players ORDER BY totallevel DESC")
		results = self.cursor.fetchall()
		self.ranks = []

		for steamid in results:
			self.ranks.append(steamid[0])

	def getRank(self, steamid):
		if steamid in self.ranks:
			return self.ranks.index(steamid) + 1
		return self.__len__()

	def removeWarnings(self, value):
		return str(value).replace("'", "").replace('"', '')
#database = SQLiteManager(Path(es.getAddonPath('wcs')))
database = SQLiteManager(Path(ini.path).joinpath('data'))


tmp = {}
#def getPlayer(userid):
#def getPlayer(userid, steamid, name):
def getPlayer(userid):
	userid = int(userid)
	if not userid in tmp:
		tmp[userid] = PlayerObject(userid)
		#tmp[userid] = PlayerObject(userid, steamid, name)
	return tmp[userid]


class PlayerObject(object):
	#def __init__(self, userid, steamid, name):
	def __init__(self, userid):
		self.userid             = userid
		if not es.exists('userid', self.userid):
			logging.log('wcs: Error: Unknown userid: '+str(self.userid))
			raise NotImplementedError, 'Unknown userid: '+str(self.userid)
		self.steamid            = playerlib.uniqueid(self.userid, True)
		#self.steamid            = steamid
		self.UserID             = database.getUserIdFromSteamId(self.steamid)

		if self.UserID is None:
			self.UserID         = database.addPlayer(self.steamid, es.getplayername(self.userid))
			#self.UserID         = database.addPlayer(self.steamid, name)

		self.player             = _getPlayer(self.userid, self.UserID)
		#self.race               = Race(self.UserID, self.player.getInfo('currace'))
		self.race               = _getRace(self.UserID, self.player.currace, self.userid)

	def __del__(self):
		self.save()

	def __str__(self):
		return str(self.userid)

	def __int__(self):
		return self.userid

	def save(self):
		self.player.save()
		self.race.save()

	def changeRace(self, race, kill=True):
		self.race.save()

		if self.race.racedb['onchange']:
			es.ServerVar('wcs_userid').set(self.userid)
			es.server.insertcmd(self.race.racedb['onchange'])

		oldrace = self.player.currace

		self.player.currace = str(race)

		self.race = _getRace(self.UserID, race, self.userid)
		self.race.update()
		self.race.refresh()
		self.race.save()

		if kill:
			expand.damage(self.userid, '#health', self.userid)
			#if es.isbot(self.userid):
			#	es.server.queuecmd('bot_kill '+es.getplayername(self.userid))
			#else:
			#	es.server.queuecmd('es_xsexec '+str(self.userid)+' kill')

		events.Event('wcs_changerace').set({'userid':self.userid,'oldrace':oldrace,'newrace':race}).fire()

	def giveXp(self, amount, reason=''):
		return self.race.addXp(amount, reason)

	def giveLevel(self, amount):
		return self.race.addLevel(amount)

	def giveUnused(self, amount):
		return self.race.addUnused(amount)

	def givePoint(self, skill):
		return self.race.addPoint(skill)

	def showXp(self):
		xp         = self.race.xp
		level      = self.race.level
		needed     = int(cfgdata['interval'])*level if level else int(cfgdata['interval'])
		race       = self.player.currace

		tell(self.userid, 'main: xp needed', {'race':race,'level':level,'xp':xp,'needed':needed})

	def showRank(self):
		name       = self.player.name
		race       = self.player.currace
		level      = self.race.level
		place      = database.getRank(self.steamid)
		total      = str(len(database))
		xp         = self.race.xp
		needed     = int(cfgdata['interval'])*level if level else int(cfgdata['interval'])
		unused     = self.race.unused

		for user in es.getUseridList():
			tell(user, 'main: show rank', {'name':name,'race':race,'level':level,'place':place,'total':total,'xp':xp,'needed':needed,'unused':unused})

	def delRace(self):
		self.player.totallevel -= int(self.race.level)
		database.execute("DELETE FROM Races WHERE UserID = ? AND name = ?", (self.UserID, self.player.currace))
		self.race.level = 0
		self.race.xp = 0
		self.race.skills = ''
		self.race.unused = 0
		self.race.refresh()
		self.race.save()
		#self.race = _getRace(self.UserID, self.player.currace, self.userid)

	def delPlayer(self):
		database.execute('DELETE FROM Players WHERE UserID = ?', (self.player.UserID, ))
		database.execute('DELETE FROM Races WHERE UserID = ?', (self.player.UserID, ))

		del tmp1[self.userid]
		del tmp2[self.userid]

		self.player = _getPlayer(self.userid, self.UserID)
		self.race = _getRace(self.UserID, self.player.currace, self.userid)

		#self.player.save()
		#self.player.update()

		#self.race.update()
		self.race.refresh()
		#self.race.save()

		#self.__init__(self.userid)
info.name = 'Wcs'

tmp1 = {}
def _getPlayer(userid, UserID):
	userid = int(userid)
	if not userid in tmp1:
		tmp1[userid] = Player(userid, UserID)

	return tmp1[userid]

class Player(object):
	def __init__(self, userid, UserID):
		self.userid = userid
		self.UserID = UserID
		self.update()

	def update(self):
		self.steamid, self.currace, self.name, self.totallevel, self.lastconnect = self._getInfo(('steamid',
																								  'currace',
																								  'name',
																								  'totallevel',
																								  'lastconnect'))

		self.name = database.removeWarnings(self.name)

	def save(self):
		try:
			self._setInfo({'steamid':self.steamid,
						   'currace':self.currace,
						   'name':self.name,
						   'totallevel':self.totallevel,
						   'lastconnect':self.lastconnect})
		except:
			logging.log('wcs: Information: Unable to set information for UserID '+str(self.UserID))
			logging.log('wcs: Information: Error message: '+str(sys.exc_info()[1]))
			logging.log('wcs: Information: Possible errors: '+str(self.steamid)+' '+str(self.currace)+' '+str(self.name)+' '+str(self.totallevel)+' '+str(self.lastconnect))

	def _getInfo(self, what):
		if not hasattr(what, '__iter__'):
			what = (what, )

		database.execute("SELECT "+','.join(map(str, what))+" FROM Players WHERE UserID = ?", (self.UserID, ))

		v = database.fetchone()
		if v is None:
			return (es.getplayersteamid(self.userid), standardrace, es.getplayername(self.userid), 0, time.time())

		return v

	def _setInfo(self, options):
		keys = []
		for option, value in options.iteritems():
			keys.append((option+"='"+str(value)+"'"))

		database.execute("UPDATE Players SET " + ','.join(keys) + " WHERE UserID = ?", (self.UserID, ))

tmp2 = {}
def _getRace(userid, race, user):
	user = int(user)
	if not user in tmp2:
		tmp2[user] = {}

	if not race in tmp2[user]:
		tmp2[user][race] = Race(userid, race, user)

	return tmp2[user][race]

class Race(object):
	def __init__(self, UserID, race, user):
		self.userid     = user
		self.steamid    = es.getplayersteamid(self.userid)
		self.UserID     = UserID
		self.player     = _getPlayer(self.userid, self.UserID)

		if not race in racedb:
			tell(self.userid, 'main: race no found', {'race':race})
			#es.tell(self.userid, '#multi', '#greenIt seems like your current race ('+race+') is #lightgreennot #greenin the database.')
			logging.log('wcs: Information: Unknown race ('+race+') found on UserID '+str(self.UserID))
			race = standardrace
			self.player.currace = standardrace

		self.RaceID     = database.getRaceIdFromUserIdAndRace(self.UserID, race)
		if self.RaceID is None:
			self.RaceID = database.addRaceIntoPlayer(self.UserID, race)

		self.racedb = racedb.getRace(race)

		self.update()
		self.refresh()

	def __contains__(self, race):
		if isinstance(race, int):
			database.execute("SELECT RaceID FROM Races WHERE UserID = ? AND RaceID = ?", (self.UserID, race))
		else:
			database.execute("SELECT RaceID FROM Races WHERE UserID = ? AND name = ?", (self.UserID, race))
		return database.fetchone()

	def update(self):
		self.name, self.skills, self.level, self.xp, self.unused = self._getInfo(('name',
																				  'skills',
																				  'level',
																				  'xp',
																				  'unused'))

	def save(self):
		try:
			self._setInfo({'name':self.name,
						  'skills':self.skills,
						  'level':self.level,
						  'xp':self.xp,
						  'unused':self.unused})
		except:
			logging.log('wcs: Information: Unable to set information for UserID '+str(self.UserID))
			logging.log('wcs: Information: Error message: '+str(sys.exc_info()[1]))
			logging.log('wcs: Information: Possible errors: '+str(self.name)+' '+str(self.skills)+' '+str(self.level)+' '+str(self.xp)+' '+str(self.unused))

	def refresh(self):
		if not self.skills or self.skills is None or self.skills == 'None':
			skills = []
			for x in xrange(1,10):
				skill = 'skill'+str(x)
				if skill in self.racedb:
					skills.append('0')

			self.skills = '|'.join(skills)

	def _getInfo(self, what):
		if not hasattr(what, '__iter__'):
			what = (what, )

		database.execute("SELECT "+','.join(map(str, what))+" FROM Races WHERE UserID = ? AND RaceID = ?", (self.UserID, self.RaceID))

		v = database.fetchone()
		if v is None:
			return (self.player.currace, '', 0, 0, 0)

		return v

	def _setInfo(self, options):
		keys = []
		for option, value in options.iteritems():
			keys.append((option+"='"+str(value)+"'"))

		database.execute("UPDATE Races SET " + ','.join(keys) + " WHERE UserID = ? AND RaceID = ?", (self.UserID, self.RaceID))


	def addXp(self, amount, reason=''):
		amount = int(amount)
		if not amount:
			return

		currentXp = self.xp + amount

		amountOfLevels = 0
		nextLevelXp = int(cfgdata['interval'])*self.level if self.level else int(cfgdata['interval'])

		while currentXp >= nextLevelXp:
			amountOfLevels += 1
			currentXp -= nextLevelXp
			nextLevelXp += int(cfgdata['interval'])

		self.xp = currentXp

		if es.exists('userid', self.userid):
			tell(self.userid, 'main: gain xp', {'amount':amount}, (' '+reason) if reason else '')

		if amountOfLevels:
			self.addLevel(amountOfLevels)

		events.Event('wcs_gainxp').set({'userid':self.userid,'amount':amount,'levels':amountOfLevels,'currentxp':self.xp,'reason':reason}).fire()

		return currentXp

	def addLevel(self, amount):
		amount = int(amount)
		if not amount:
			return

		self.level += amount
		self.unused += amount
		self.player.totallevel += amount

		if 'BOT' in self.steamid:
			maxlevel = int(self.racedb['numberoflevels'])

			while True:
				if not self.unused:
					break

				possibleChoices = []
				skills = self.skills.split('|')

				if len(skills):
					if skills[0] == '':
						self.raceUpdate()

				for skill, level in enumerate(skills):
					if int(skills[skill]) < maxlevel:
						possibleChoices.append(str(skill+1))

				if not len(possibleChoices):
					break

				choice = random.choice(possibleChoices)
				self.addPoint(choice)

		else:
			if es.exists('userid', self.userid):
				tell(self.userid, 'main: level gain', {'level':self.level,'xp':self.xp,'needed':self.level*int(cfgdata['interval'])})

				gamethread.delayed(2, sendPopup, (spendskills.doCommand, self.userid))
				#gamethread.delayed(2, spendskills.doCommand, self.userid)

		if es.exists('userid', self.userid):
			if es.getplayerprop(self.userid, 'CBasePlayer.pl.deadflag'):
				es.playsound(self.userid, 'ambient/machines/teleport1.wav', 0.4)
			else:
				es.emitsound('player', self.userid, 'ambient/machines/teleport1.wav', 0.8, 0.3)

				if graphicfx:
					x,y,z = es.getplayerlocation(self.userid)
					effect.effect.BlueCircle((x,y,z+38), BaseSpread=28, Rate=173, RenderColor=(252,232,131), Twist=15, Delayed=3.5, Userid=self.userid)

		events.Event('wcs_levelup').set({'userid':self.userid,'race':self.name,'oldlevel':self.level-amount,'newlevel':self.level,'amount':amount}).fire()

		return self.level

	def addUnused(self, amount):
		self.unused += amount
		return self.unused

	def addPoint(self, skill):
		skills = self.skills.split('|')
		index = int(skill)-1
		level = int(skills[index])

		if self.unused:
			skills.pop(index)
			skills.insert(index, str(level+1))

			self.skills = '|'.join(skills)

			self.unused -= 1

			return level+1

class cmdlibRegister(object):
	def __init__(self):
		self.timed = {}

	@staticmethod
	def changerace(userid, args=None):
		changerace.doCommand(userid, 'changerace')

	@staticmethod
	def showxp(userid, args=None):
		getPlayer(userid).showXp()

	@staticmethod
	def playerinfo(userid, args=None):
		playerinfo.doCommand(userid)

	@staticmethod
	def wcsrank(userid, args=None):
		wcstop.wcsRank(userid, ' '.join(map(str, args)))

	@staticmethod
	def wcstop(userid, args=None):
		wcstop.doCommand(userid, 'wcstop')

	@staticmethod
	def spendskills(userid, args=None):
		spendskills.doCommand(userid)

	@staticmethod
	def resetskills(userid, args=None):
		resetskills.doCommand(userid)

	@staticmethod
	def wcsmenu(userid, args=None):
		wcsmenu.doCommand(userid)

	@staticmethod
	def wcshelp(userid, args=None):
		wcshelp.doCommand(userid)

	@staticmethod
	def raceinfo(userid, args=None):
		raceinfo.doCommand(userid, 'raceinfo0', False)

	@staticmethod
	def savexp(userid, args=None):
		savexp.doCommand(userid)

	@staticmethod
	def showskills(userid, args=None):
		showskills.doCommand(userid)

	@staticmethod
	def shopmenu(userid, args=None):
		if allowshopmenu:
			shopmenu.doCommand(userid, 'shopmenu')

	@staticmethod
	def shopinfo(userid, args=None):
		if allowshopmenu:
			shopinfo.doCommand(userid)

	def reloadRaces(self, args):
		if not 'reload' in self.time:
			self.time['reload'] = time.time()

		if time.time()-self.time['reload'] <= 180:
			racedb.races = ini.getRaces
			self.time['reload'] = time.time()
			logging.log('wcs: Information: Successfully reloaded the races.ini file')
cmdreg = cmdlibRegister()


class CfgManager(object):
	def __init__(self, name):
		self.name = name

		self.cfg = cfglib.AddonCFG(os.path.join(ini.path, 'config', self.name+'.cfg'))

	def __getattr__(self, attr):
		return getattr(self.cfg, attr)


class EventManager(object):
	def __init__(self, file):
		self.file = str(file)+'.res' if not str(file).endswith('.res') else ''
		self.load()

	def load(self):
		es.loadevents('declare', 'addons/eventscripts/wcs/events/'+self.file)

	def Event(self, event):
		return Event(event)


class Event(object):
	def __init__(self, name):
		self.name = name
		es.event('initialize', self.name)

	def set(self, options={}):
		for item, value in options.iteritems():
			if str(value).isdigit():
				es.event('setint', self.name, item, int(value))
			else:
				try:
					es.event('setfloat', self.name, item, float(value))
				except ValueError:
					if value:
						es.event('setstring', self.name, item, str(value))
					else:
						es.event('setstring', self.name, item, '0')

		return self

	def fire(self):
		es.event('fire', self.name)

	def cancel(self):
		es.event('cancel', self.name)





def player_changename(ev):
	if es.exists('userid', ev['userid']):
		getPlayer(ev['userid']).player.name = database.removeWarnings(ev['newname'])

def player_activate(ev):
	userid = str(ev['userid'])
	if es.exists('userid', userid):
		player = getPlayer(userid)
		player.player.name = database.removeWarnings(ev['es_username'])

		if not str(ev['es_steamid']).lower() == 'bot':
			if welcomeguitext and player.player.totallevel <= disabletextonlvl:
				gamethread.delayed(5, sendPopup, (welcome.doCommand, userid))
				#gamethread.delayed(5, welcome.doCommand, userid)
			if welcometext and player.player.totallevel <= disabletextonlvl:
				gamethread.delayed(10, tell, (userid, 'main: welcome'))

		wcsgroup.addUser(userid)

def player_disconnect(ev):
	userid = int(ev['userid'])

	if userid in tmp:
		tmp[userid].player.lastconnect = time.time()
		tmp[userid].player.name = database.removeWarnings(ev['es_username'])
		tmp[userid].save()
		tmp1[userid].save()
		for x in tmp2[userid]:
			tmp2[userid][x].save()

		del tmp[userid]
		del tmp1[userid]
		del tmp2[userid]

	wcsgroup.delUser(userid)

def round_start(ev):
	for user in es.getUseridList():
		if int(es.getplayerteam(user)) >= 2:
			race = getPlayer(user).player.currace
			raceinfo = racedb.getRace(race)
			if raceinfo['roundstartcmd']:
				es.server.insertcmd(raceinfo['roundstartcmd'])

	dod_round_start(ev)

saved = 0

def round_end(ev):
	for user in es.getUseridList():
		if int(es.getplayerteam(user)) >= 2:
			race = getPlayer(user).player.currace
			raceinfo = racedb.getRace(race)
			if raceinfo['roundendcmd']:
				es.server.insertcmd(raceinfo['roundendcmd'])

	dod_round_start(ev)

	if xpsaver:
		global saved
		if xpsaver >= saved:
			for x in tmp:
				tmp[x].save()

			for x in tmp1:
				tmp1[x].save()

			for x in tmp2:
				for q in tmp2[x]:
					tmp2[x][q].save()

			database.save()
			saved = 0

		else:
			saved += 1

def round_freeze_end(ev):
	dod_round_active(ev)

def dod_round_start(ev):
	global gamestarted
	gamestarted = 0
	es.ServerVar('wcs_gamestarted').set(0)

def dod_round_active(ev):
	global gamestarted
	gamestarted = 1
	es.ServerVar('wcs_gamestarted').set(1)

def player_death(ev):
	victim = int(ev['userid'])
	attacker = int(ev['attacker'])

	if attacker and victim and es.exists('userid', victim) and es.exists('userid', attacker):
		player = getPlayer(victim)

		if not victim == attacker:
			if not ev['es_userteam'] == ev['es_attackerteam']:
				if (not (ev['es_steamid'] == 'BOT' and not allowbotsreward)) and (not (ev['es_attackersteamid'] == 'BOT' and not allowbotsgetxp)):
					player1 = getPlayer(attacker)
					bonus = 0
					if player1.race.level < player.race.level:
						diffience = player.race.level - player1.race.level
						bonus = diffience * int(cfgdata['bonusxp'])

					if bonus:
						gamethread.delayed(1, player1.giveXp, (int(cfgdata['killxp'])+bonus, strings('main: reason: higher level', {'diffience':diffience}, playerlib.getPlayer(attacker).get('lang'))))
					else:
						gamethread.delayed(1, player1.giveXp, (int(cfgdata['killxp']), strings('main: reason: make kill', {}, playerlib.getPlayer(attacker).get('lang'))))

					if ev['headshot'] == '1':
						gamethread.delayed(1, player1.giveXp, (int(cfgdata['headshotxp']), strings('main: reason: make headshot', {}, playerlib.getPlayer(attacker).get('lang'))))
					elif ev['weapon'] == 'knife':
						gamethread.delayed(1, player1.giveXp, (int(cfgdata['knifexp']), strings('main: reason: make knife', {}, playerlib.getPlayer(attacker).get('lang'))))

				if int(cfgdata['allow_player_death']):
					checkEvent(victim, 'player_death')
				if int(cfgdata['allow_player_kill']):
					checkEvent(attacker, 'player_kill')

		if player.race.racedb['deathcmd']:
			es.server.insertcmd(raceinfo['deathcmd'])

	if victim and es.exists('userid', victim):
		for i, v in {'gravity':1.0,'speed':1.0,'longjump':0}.iteritems():
			wcsgroup.setUser(victim, i, v)

		expand.gravity(victim, 1)

		playerlib.getPlayer(victim).setColor(255, 255, 255, 255)

	if removeragdolls:
		if ragdoll:
			es.fire(es.getuserid(), ragdoll, 'kill')


def player_hurt(ev):
	victim = int(ev['userid'])
	attacker = int(ev['attacker'])

	if attacker and victim and es.exists('userid', victim) and es.exists('userid', attacker) and not ev['weapon'].lower() in ('point_hurt'):
		if not victim == attacker:
			if not ev['es_userteam'] == ev['es_attackerteam']:
				if int(cfgdata['allow_player_victim']):
					checkEvent(victim, 'player_victim')
				if int(cfgdata['allow_player_attacker']):
					checkEvent(attacker, 'player_attacker')

		if int(cfgdata['allow_player_hurt']):
			checkEvent(victim, 'player_hurt')
			checkEvent(attacker, 'player_hurt')



def player_spawn(ev):
	userid = int(ev['userid'])
	team = int(ev['es_userteam'])

	if userid and team >= 2 and es.exists('userid', userid):
		for i, v in {'gravity':1.0,'speed':1.0,'longjump':0}.iteritems():
			wcsgroup.setUser(userid, i, v)

		expand.gravity(userid, 1)

		playerlib.getPlayer(userid).setColor(255, 255, 255, 255)

		player = getPlayer(userid)

		if not str(ev['es_steamid']).lower() == 'bot':
			if spawntext and player.player.totallevel <= disabletextonlvl:
				tell(userid, 'main: help text')

		wcsgroup.addUser(userid)

		player.showXp()

		#player.raceUpdate()
		if int(cfgdata['allow_player_spawn']):
			checkEvent(userid, 'player_spawn')

		race = player.player.currace
		raceinfo = racedb.getRace(race)
		if int(raceinfo['restrictteam']) and not ev['es_steamid'] == 'BOT':
			if team == int(raceinfo['restrictteam']) and team >= 2 and not ev['es_steamid'] == 'BOT':
				tell(userid, 'main: race restricted team', {'race':race, 'team':{2:'T',3:'CT'}[team]})
				es.server.queuecmd('es_xchangeteam '+str(userid)+' 1')
				#es.changeteam(userid, 1)
				changerace.doCommand(userid, 'changerace')
				wcsgroup.setUser(userid, 'restrictteam', team)

		elif 'teamlimit' in raceinfo and not ev['es_steamid'] == 'BOT':
			q = int(raceinfo['teamlimit'])
			if q:
				v = wcsgroup.getUser({2:'T',3:'CT'}[team], 'restricted')
				if v > q:
					tell(userid, 'main: race team limit', {'race':race, 'team':{2:'T',3:'CT'}[team]})
					es.server.queuecmd('es_xchangeteam '+str(userid)+' 1')
					#es.changeteam(userid, 1)
					changerace.doCommand(userid, 'changerace')
					#wcsgroup.setUser(userid, 'restricted', team)

		elif curmap in raceinfo['restrictmap'].split('|'):
			if not ev['es_steamid'] == 'BOT':
					tell(userid, 'main: race restricted map', {'race':race, 'map':curmap})
					es.server.queuecmd('es_xchangeteam '+str(userid)+' 1')
					#es.changeteam(userid, 1)
					changerace.doCommand(userid, 'changerace')
					#wcsgroup.setUser(userid, 'restricted', team)

		if raceinfo['spawncmd']:
			es.server.insertcmd(raceinfo['spawncmd'])

def server_shutdown(ev):
	for x in es.getUseridList():
		savexp.doCommand(x, False)

	tmp.clear()
	tmp1.clear()
	tmp2.clear()

	database.save()
	database.close()

def backwards(name):
	return dstr(dstr(dstr(name)))

def player_say(ev):
	userid = ev['userid']

	if int(cfgdata['allow_player_say']):
		checkEvent(userid, 'player_say')

DATABASE_STORAGE_METHOD = SQLiteManager



raceevents = {}
aliass = {}
database = None
databasePath = Path(ini.path).joinpath('data')
events = EventManager('events')

def load():
	global database
	config.execute()

	database = DATABASE_STORAGE_METHOD(databasePath)

	database.updateRank()

	admin.admins.load()
	group.groups.load()

	cmdlib.registerClientCommand('changerace',  cmdreg.changerace,  '')
	cmdlib.registerClientCommand('showxp',      cmdreg.showxp,      '')
	cmdlib.registerClientCommand('playerinfo',  cmdreg.playerinfo,  '')
	cmdlib.registerClientCommand('wcsrank',     cmdreg.wcsrank,     '')
	cmdlib.registerClientCommand('wcstop',      cmdreg.wcstop,      '')
	cmdlib.registerClientCommand('spendskills', cmdreg.spendskills, '')
	cmdlib.registerClientCommand('resetskills', cmdreg.resetskills, '')
	cmdlib.registerClientCommand('wcsmenu',     cmdreg.wcsmenu,     '')
	cmdlib.registerClientCommand('wcshelp',     cmdreg.wcshelp,     '')
	cmdlib.registerClientCommand('wcs',         cmdreg.wcsmenu,     '')
	cmdlib.registerClientCommand('raceinfo',    cmdreg.raceinfo,    '')
	cmdlib.registerClientCommand('savexp',      cmdreg.savexp,      '')
	cmdlib.registerClientCommand('showskills',  cmdreg.showskills,  '')
	cmdlib.registerClientCommand('shopmenu',    cmdreg.shopmenu,    '')
	cmdlib.registerClientCommand('shopinfo',    cmdreg.shopinfo,    '')
	cmdlib.registerSayCommand('changerace',     cmdreg.changerace,  '')
	cmdlib.registerSayCommand('showxp',         cmdreg.showxp,      '')
	cmdlib.registerSayCommand('playerinfo',     cmdreg.playerinfo,  '')
	cmdlib.registerSayCommand('wcsrank',        cmdreg.wcsrank,     '')
	cmdlib.registerSayCommand('wcstop',         cmdreg.wcstop,      '')
	cmdlib.registerSayCommand('spendskills',    cmdreg.spendskills, '')
	cmdlib.registerSayCommand('resetskills',    cmdreg.resetskills, '')
	cmdlib.registerSayCommand('wcsmenu',        cmdreg.wcsmenu,     '')
	cmdlib.registerSayCommand('wcshelp',        cmdreg.wcshelp,     '')
	cmdlib.registerSayCommand('wcs',            cmdreg.wcsmenu,     '')
	cmdlib.registerSayCommand('raceinfo',       cmdreg.raceinfo,    '')
	cmdlib.registerSayCommand('savexp',         cmdreg.savexp,      '')
	cmdlib.registerSayCommand('showskills',     cmdreg.showskills,  '')
	cmdlib.registerSayCommand('shopmenu',       cmdreg.shopmenu,    '')
	cmdlib.registerSayCommand('shopinfo',       cmdreg.shopinfo,    '')

	cmdlib.registerServerCommand('wcs_reload_races', cmdreg.reloadRaces, 'Will reload to races.ini file')

	es.load('wcs/tools')
	es.load('wcs/addons')

	if os.path.isdir(os.path.join(ini.path, 'extension', game)):
		es.load('wcs/extension/'+game)
	es.ServerVar('wcs_game').set(game)

	races = racedb.getAll()
	es.ServerVar('wcs_version',   version,    'Warcraft: Source version - Made by Tha Pwned original by Kryptonite').makepublic()
	es.ServerVar('wcs_author',    author,     'The authors of WCS').makepublic()
	es.ServerVar('wcs_racecount', len(races), 'The amount of races on the server').makepublic()

	global curmap
	curmap = es.ServerVar('eventscripts_currentmap')
	es.ServerVar('wcs_gamestarted').set(curmap)

	global aliass
	for race in races:
		for section in races[race]:
			if 'racealias_' in section:
				if section in aliass:
					logging.log('wcs: Error: The racealias '+section+' is already in use')
				else:
					aliass[section] = str(races[race][section])

			if section == 'skillcfg':
				global raceevents
				if not race in raceevents:
					raceevents[race] = {}

				events = races[race]['skillcfg'].split('|')

				for index, cfg in enumerate(events):
					if not cfg in raceevents[race]:
						raceevents[race][cfg] = []

					raceevents[race][cfg].append(str(index))

			elif section == 'preloadcmd':
				es.server.insertcmd(races[race]['preloadcmd'])

			if 'skill' in section:
				for y in races[race][section]:
					if 'racealias_' in y:
						if y in aliass:
							logging.log('wcs: Error: The racealias '+y+' is already in use')
						else:
							aliass[y] = str(races[race][section][y])

	items = ini.getItems
	for section in items:
		for item in items[section]:
			for q in items[section][item]:
				if 'shopalias_' in q:
					if q in aliass:
						logging.log('wcs: Error: The shopalias '+q+' is already in use')
					else:
						aliass[q] = str(items[section][item][q])

	if es.getplayercount():
		es.server.queuecmd('mp_restartgame 2')

	global gamestarted
	gamestarted = 0
	es.ServerVar('wcs_gamestarted').set(0)

	tag = es.ServerVar('sv_tags')
	if not 'wcs' in str(tag):
		v = str(tag).split(',')
		v.append('wcs')
		tag.set(','.join(v))

info.version  = version
def unload():
	if os.path.isdir(os.path.join(ini.path, 'extension', game)):
		es.unload('wcs/extension/'+game)

	#for userid in es.getUseridList():
	#	cmdreg.savexp(userid, '')

	for x in es.getUseridList():
		savexp.doCommand(x, False)

	tmp.clear()
	tmp1.clear()
	tmp2.clear()

	for x in getPopups():
		if popuplib.exists(x):
			popuplib.close(x, es.getUseridList())
			popuplib.delete(x)

	database.save()
	database.close()

	cmdlib.unregisterClientCommand('changerace')
	cmdlib.unregisterClientCommand('showxp')
	cmdlib.unregisterClientCommand('playerinfo')
	cmdlib.unregisterClientCommand('wcsrank')
	cmdlib.unregisterClientCommand('wcstop')
	cmdlib.unregisterClientCommand('spendskills')
	cmdlib.unregisterClientCommand('resetskills')
	cmdlib.unregisterClientCommand('wcsmenu')
	cmdlib.unregisterClientCommand('wcshelp')
	cmdlib.unregisterClientCommand('wcs')
	cmdlib.unregisterClientCommand('raceinfo')
	cmdlib.unregisterClientCommand('savexp')
	cmdlib.unregisterClientCommand('showskills')
	cmdlib.unregisterClientCommand('shopmenu')
	cmdlib.unregisterClientCommand('shopinfo')
	cmdlib.unregisterSayCommand('changerace')
	cmdlib.unregisterSayCommand('showxp')
	cmdlib.unregisterSayCommand('playerinfo')
	cmdlib.unregisterSayCommand('wcsrank')
	cmdlib.unregisterSayCommand('wcstop')
	cmdlib.unregisterSayCommand('spendskills')
	cmdlib.unregisterSayCommand('resetskills')
	cmdlib.unregisterSayCommand('wcsmenu')
	cmdlib.unregisterSayCommand('wcshelp')
	cmdlib.unregisterSayCommand('wcs')
	cmdlib.unregisterSayCommand('raceinfo')
	cmdlib.unregisterSayCommand('savexp')
	cmdlib.unregisterSayCommand('showskills')
	cmdlib.unregisterSayCommand('shopmenu')
	cmdlib.unregisterSayCommand('shopinfo')

	cmdlib.unregisterServerCommand('wcs_reload_races')

	es.unload('wcs/tools')
	es.unload('wcs/addons')

	admin.admins.save()
	admin.admins.close()
	group.groups.save()
	group.groups.close()

	tag = es.ServerVar('sv_tags')
	if 'wcs' in str(tag):
		v = str(tag).split(',')
		v.remove('wcs')
		tag.set(','.join(v))
info.basename = info.name.lower()

def es_map_start(ev):
	for x in es.getUseridList():
		savexp.doCommand(x, False)

	database.save()

	if ev['mapname']:
		global curmap
		curmap = ev['mapname']

	database.updateRank()

	events.load()

	admin.admins.close()
	admin.admins.load()
	group.groups.close()
	group.groups.load()

def checkEvent(userid, event):
	logging.log('wcs: Information: Firing event: '+event, 4)
	if es.exists('userid', userid):
		if int(playerlib.getPlayer(userid).team) > 1:
			player = getPlayer(userid)
			race = player.player.currace
			race1 = racedb.getRace(race)
			logging.log('wcs: Information: Found race '+race, 4)
			if event in raceevents[race]:
				logging.log('wcs: Information: Found event '+event+' in race '+race, 5)
				skills = player.race.skills.split('|')
				logging.log('wcs: Information: Checking skills...', 4)
				for index in raceevents[race][event]:
					logging.log('wcs: Information: Found skill '+str(int(index)+1), 4)
					level = int(skills[int(index)])
					if level:
						logging.log('wcs: Information: True level', 4)
						es.ServerVar('wcs_userid').set(userid)
						es.ServerVar('wcs_dice').set(random.randint(0, 100))
						skill = 'skill'+str(int(index)+1)

						try:
							if race1[skill]['setting'].split('|')[level-1]:
								es.server.insertcmd(race1[skill]['setting'].split('|')[level-1])
						except IndexError:
							logging.log('wcs: Error: '+skill+' on race '+race+' is not correct!')
							continue

						if 'cmd' in race1[skill]:
							if race1[skill]['cmd']:
								es.server.insertcmd(race1[skill]['cmd'])
						elif 'block' in race1[skill]:
							if race1[skill]['block']:
								es.doblock(race1[skill]['block'])
						else:
							logging.log('wcs: Error: Missing cmd- or block-key on race '+race+' inside skill '+skill)
							continue

						if race1[skill]['sfx']:
							es.server.insertcmd(race1[skill]['sfx'])

def checkEvent1(userid, event):
	logging.log('wcs: Information: Firing event: '+event, 4)
	if es.exists('userid', userid):
		if int(playerlib.getPlayer(userid).team) > 1:
			player = getPlayer(userid)
			race = player.player.currace
			race1 = racedb.getRace(race)
			logging.log('wcs: Information: Found race '+race, 4)
			if event in raceevents[race]:
				logging.log('wcs: Information: Found event '+event+' in race '+race, 5)
				skills = player.race.skills.split('|')
				logging.log('wcs: Information: Checking skills...', 4)
				index = raceevents[race][event][0]
				logging.log('wcs: Information: Found skill '+str(int(index)+1), 4)
				level = int(skills[int(index)])
				if level:
					if gamestarted:
						logging.log('wcs: Information: True level', 4)
						es.ServerVar('wcs_userid').set(userid)
						es.ServerVar('wcs_dice').set(random.randint(0, 100))
						skill = 'skill'+str(int(index)+1)
						cooldown = wcsgroup.getUser(userid, event+'_cooldown')
						if cooldown is None:
							cooldown = 0
						cooldown = int(cooldown)
						wcsgroup.setUser(userid, event+'_pre_cooldown', cooldown)

						timed = int(float(time.time()))
						downtime = str(race1[skill]['cooldown']).split('|')
						if len(downtime) == int(player.race.racedb['numberoflevels']):
							downtime = int(downtime[int(player.race.racedb['numberoflevels'])-1])
						else:
							downtime = int(downtime[0])

						logging.log('wcs: Information: Checking cooldown...', 4)
						if not downtime or (timed - cooldown >= downtime):
							logging.log('wcs: Information: True cooldown', 4)
							if race1[skill]['setting']:
								try:
									if race1[skill]['setting'].split('|')[level-1]:
										es.server.insertcmd(race1[skill]['setting'].split('|')[level-1])
								except IndexError:
									logging.log('wcs: Error: '+skill+' on race '+race+' is not correct!')
									return

							var = 'wcs_'+event.replace('player_', '')[:4]+'notexec'
							es.ServerVar(var).set(0)

							if 'cmd' in race1[skill]:
								if race1[skill]['cmd']:
									es.server.insertcmd(race1[skill]['cmd'])
							elif 'block' in race1[skill]:
								if race1[skill]['block']:
									es.doblock(race1[skill]['block'])
							else:
								logging.log('wcs: Error: Missing cmd- or block-key on race '+race+' inside skill '+skill)
								return

							if race1[skill]['sfx']:
								es.server.insertcmd(race1[skill]['sfx'])

							#Doesn't seems to work. It takes 1 tick for the variable to be set.
							if int(es.ServerVar(var)):
								#Skill was stopped by wcs_<var>notexec (so, don't set the cooldown)
								return

							wcsgroup.setUser(userid, event+'_cooldown', timed)
							#Success
							return (1, downtime, timed-cooldown)
						#Cooldown
						return (0, downtime, timed-cooldown)
					#Game has not started
					return False
	return None

def tell(userid, text, tokens={}, extra='', lng=True):
	if str(userid).startswith('#'):
		userid = playerlib.getPlayerList(userid)

	if not userid:
		return

	if not hasattr(userid, '__iter__'):
		if not es.exists('userid', userid):
			return

		userid = (userid, )

	for user in userid:
		if es.exists('userid', user) and not es.isbot(user):
			if lng:
				try:
					text = strings(text, tokens, langlib.getLangAbbreviation(es.getclientvar(user, 'cl_language')))
				except:
					logging.log('wcs: There was a error when trying to find the text "'+str(text)+'"')
					sys.excepthook(*sys.exc_info())
					return

			if not text:
				continue

			if len(extra):
				if '#darkgreen' in text or '#darkgreen' in extra:
					es.tell(userid, '#multi', str(text%extra).replace('#darkgreen', '\x05'))
				else:
					saytextlib.sayText2(userid, es.getindexfromhandle(es.getplayerhandle(userid)), str(text%extra))
			else:
				if '%s' in text:
					text = text.replace('%s', '')

				if '#darkgreen' in text:
					es.tell(userid, '#multi', text.replace('#darkgreen', '\x05'))
				else:
					saytextlib.sayText2(userid, es.getindexfromhandle(es.getplayerhandle(user)), text)

def getPopups():
	modules = [admin, changerace, dataAPI, effect, expand, group, keyAPI, playerinfo, raceinfo, resetskills, savexp, shopinfo, shopmenu, showskills, spendskills, sqliteAPI, wcsgroup, wcshelp, wcsmenu, wcstop, welcome]
	popupslist = []
	for x in modules:
		if hasattr(x, 'getPopups'):
			for x in getattr(x, 'getPopups')():
				popupslist.append(x)

	return popupslist

def sendPopup(name, userid, args=''):
	if es.exists('userid', userid):
		if callable(name):
			if args:
				name(userid, args)
			else:
				name(userid)
		else:
			popuplib.send(userid, name)

def cancel(userid, what):
	wcsgroup.setUser(userid, what+'_cooldown', wcsgroup.getUser(userid, what+'_pre_cooldown'))
