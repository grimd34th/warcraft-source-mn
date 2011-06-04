import es
import cmdlib

import os.path

from configobj import ConfigObj

from wcs import wcs


cfg = wcs.CfgManager('wce')



class InI(object):
	def __init__(self):
		self.items = str(os.path.join(wcs.ini.path, 'ini', 'wce.ini'))

	@property
	def getShopItems(self):
		return ConfigObj(self.items)['shopitems']

	@property
	def getCollectItems(self):
		return ConfigObj(self.items)['collectitems']
ini = InI()

class ShopItems(object):
	def __init__(self):
		self.load()

	def __contains__(self, item):
		return item in self.data

	def __iter__(self):
		return self.data.__iter__()

	def __len__(self):
		return len(self.data)

	def __getitem__(self, item):
		return self.data[item]

	def load(self):
		self.data = ini.getShopItems
SI = ShopItems()

class CollectItems(object):
	def __init__(self):
		self.load()
		self.chance = []

	def __contains__(self, item):
		return item in self.data

	def __iter__(self):
		return self.data.__iter__()

	def __len__(self):
		return len(self.data)

	def __getitem__(self, item):
		return self.data[item]

	def load(self):
		self.data = ini.getCollectItems

	def chance(self):
		if not self.chance:
			for x in self.data:
				q = self.data[x]['count']
				while q > 0:
					q -= 1
					self.chance.append(x)

		return self.chance
CI = CollectItems()


class SQLiteManager(wcs.sqliteAPI.SQLiteAPI):
	def create(self):
		self.execute("""\
			CREATE TABLE IF NOT EXISTS Players (
				UserID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				steamid       VARCHAR(30) NOT NULL,
				level         INTEGER DEFAULT 0,
				xp            INTEGER DEFAULT 0,
				cmana         INTEGER DEFAULT 100,
				rmana         INTEGER DEFAULT 5,
				mmana         INTEGER DEFAULT 100,
				copper        INTEGER DEFAULT 0,
				silver        INTEGER DEFAULT 0,
				gold          INTEGER DEFAULT 0,
				platnum       INTEGER DEFAULT 0,
			)""")

		self.execute("CREATE INDEX IF NOT EXISTS playersIndex ON Players(steamid)")

	def getUserIdFromSteamId(self, steamid):
		self.execute("SELECT UserID FROM Players WHERE steamid = ?", (steamid, ))
		v = self.fetchone()
		if v is None:
			return None

		return v

	def addPlayer(self, steamid):
		self.execute("INSERT OR IGNORE INTO Players (steamid) VALUES (?)", (steamid, ))
		return self.cursor.lastrowid
database = SQLiteManager('wce.sqlite')


tmp = {}
def getPlayer(userid):
	userid = int(userid)
	if not userid in tmp:
		tmp[userid] = Player(userid)

	return tmp[userid]

class Player(object):
	def __init__(self, userid):
		self.userid = userid
		self.steamid = getplayersteamid(self.userid)
		self.UserID = database.getUserIdFromSteamId(self.steamid)
		if self.UserID is None:
			self.UserID = database.addPlayer(self.steamid)

		self.update()

	def __del__(self):
		self.save()

	def update(self):
		self.level,self.xp,self.cmana,self.rmana,self.mmana,self.copper,self.silver,self.gold,self.platnum = self._getInfo(('level','xp','cmana','rmana','mmana','copper','silver','gold','platnum'))

	def save(self):
		self._setInfo({'level':self.level,'xp':self.xp,'cmana':self.cmana,'rmana':self.rmana,'mmana':self.mmana,'copper':self.copper,'silver':self.silver,'gold':self.gold,'platnum':self.platnum})

	def _getInfo(self, what):
		if not hasattr(what, '__iter__'):
			what = (what, )

		database.execute("SELECT "+','.join(map(str, what))+" FROM Players WHERE UserID = ?", (self.UserID, ))

		v = database.fetchone()
		if v is None:
			return (0, 0, 0, 0, 0, 0, 0, 0, 0)
		return v

	def _setInfo(self, options):
		keys = []
		for option, value in options.iteritems():
			keys.append((option+"='"+str(value)+"'"))

		database.execute("UPDATE Players SET " + ','.join(keys) + " WHERE UserID = ?", (self.UserID, ))

	def add(self, what, amount):
		if not hasattr(self, what):
			raise AttributeError, what

		amount = int(amount)
		if not amount:
			return

		setattr(self, what, getattr(self, what)+amount)

		self.convert()

		return getattr(self, what)

	def convert(self):
		if self.copper >= 100:
			while self.copper >= 100:
				self.copper -= 100
				self.silver += 1

		if self.silver >= 100:
			while self.silver >= 100:
				self.silver -= 100
				self.gold += 1

		if self.gold >= 100:
			while self.gold >= 100:
				self.gold -= 100
				self.platnum += 1

class CmdRegister:
	@staticmethod
	def cast(userid, args):
		pass

	@staticmethod
	def cast1(userid, args):
		pass

	@staticmethod
	def cast2(userid, args):
		pass

	@staticmethod
	def cast3(userid, args):
		pass

	@staticmethod
	def cast4(userid, args):
		pass

	@staticmethod
	def cast5(userid, args):
		pass

	@staticmethod
	def nextSpell(userid, args):
		pass

	@staticmethod
	def wceinfo(userid, args):
		pass



def round_end(ev):
	if ev['winner'] == 2:
		for user in playerlib.getUseridList('#t'):
			p = getPlayer(user)
			p.add('copper', p.level*25)
	elif ev['winner'] == 3:
		for user in playerlib.getUseridList('#ct'):
			p = getPlayer(user)
			p.add('copper', p.level*25)





players = {}
cmdreg = CmdRegister()
cfg.write()

def load():
	#cfg.execute()

	database.connect()

	'''cmdlib.registerClientCommand('cast', cmdreg.cast, '')
	cmdlib.registerClientCommand('cast1', cmdreg.cast1, '')
	cmdlib.registerClientCommand('cast2', cmdreg.cast2, '')
	cmdlib.registerClientCommand('cast3', cmdreg.cast3, '')
	cmdlib.registerClientCommand('cast4', cmdreg.cast4, '')
	cmdlib.registerClientCommand('cast5', cmdreg.cast5, '')
	cmdlib.registerClientCommand('nextspell', cmdreg.nextSpell, '')
	cmdlib.registerClientCommand('wceinfo', cmdreg.wceinfo, '')

	cmdlib.registerSayCommand('cast', cmdreg.cast, '')
	cmdlib.registerSayCommand('cast1', cmdreg.cast1, '')
	cmdlib.registerSayCommand('cast2', cmdreg.cast2, '')
	cmdlib.registerSayCommand('cast3', cmdreg.cast3, '')
	cmdlib.registerSayCommand('cast4', cmdreg.cast4, '')
	cmdlib.registerSayCommand('cast5', cmdreg.cast5, '')
	cmdlib.registerSayCommand('nextspell', cmdreg.nextSpell, '')
	cmdlib.registerSayCommand('wceinfo', cmdreg.wceinfo, '')'''

	CI.chance()

def unload():
	for x in tmp:
		tmp[x].save()

	database.save()
	database.close()


def es_map_start(ev):
	for x in tmp:
		tmp[x].save()

	database.save()


def generateItem(victim, attacker):
	item = random.choice(CI.chance())










