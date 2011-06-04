from es import tell, exists, getplayername, getplayersteamid
from cmdlib import registerSayCommand, registerClientCommand, unregisterSayCommand, unregisterClientCommand
from popuplib import create, easymenu, send, find
from playerlib import uniqueid, getPlayerList
from wcs.wcs import getPlayer as wgetPlayer, admin, sqliteAPI



class SQLiteManager(sqliteAPI.SQLiteAPI):
	def create(self):
		self.execute("""\
			CREATE TABLE IF NOT EXISTS Players (
				UserID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				steamid       VARCHAR(30) NOT NULL,
				levels        INTEGER DEFAULT 0
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
database = SQLiteManager('levelbank.sqlite')


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

#	def __del__(self):
#		self.save()

	def update(self):
		self.levels = self._getInfo('levels')

	def save(self):
		self._setInfo({'levels':self.levels})

	def _getInfo(self, what):
		if not hasattr(what, '__iter__'):
			what = (what, )

		database.execute("SELECT "+','.join(map(str, what))+" FROM Players WHERE UserID = ?", (self.UserID, ))

		v = database.fetchone()
		if v is None:
			return 0
		return v

	def _setInfo(self, options):
		keys = []
		for option, value in options.iteritems():
			keys.append((option+"='"+str(value)+"'"))

		database.execute("UPDATE Players SET " + ','.join(keys) + " WHERE UserID = ?", (self.UserID, ))

	def addLevel(self, amount):
		amount = int(amount)
		if not amount:
			return

		self.levels += amount

		return self.levels


def load():
	registerClientCommand('wcsbankadmin', register, '')
	registerSayCommand('wcsbankadmin', register, '')
	registerClientCommand('wcsbank', spendslevelsCmd, '')
	registerSayCommand('wcsbank', spendslevelsCmd, '')

	popup = create('wcsbanklevel')
	popup.addline('Spend your levels here')
	popup.addline(' ')
	popup.addline(' ')
	popup.addline('->1. 1')
	popup.addline('->2. 5')
	popup.addline('->3. 10')
	popup.addline('->4. 25')
	popup.addline('->5. 100')
	popup.addline('->6. 250')
	popup.addline('->7. 1000')
	popup.addline('->8. 2500')
	popup.addline(' ')
	popup.addline('0. Close')

	popup.menuselect = menuselect

	popup.submenu(9, 'wcsbanklevel')

	database.connect()

def unload():
	tmp.clear()

	unregisterClientCommand('wcsbankadmin')
	unregisterSayCommand('wcsbankadmin')
	unregisterClientCommand('wcsbank')
	unregisterSayCommand('wcsbank')

	database.save()
	database.close()

def es_map_start(ev):
	database.save()

def register(userid, args):
	if admin.getPlayer(userid).hasFlag('wcsbankadmin'):
		menu(userid)
	else:
		tell(userid, '#multi', '#lightgreenYou\'re #greennot #lightgreenan WCS-bank admin')

def spendslevelsCmd(userid, args):
	steamid = getplayersteamid(userid)
	player = getPlayer(userid)

	if player.levels:
		popup = find('wcsbanklevel')
		popup.modline(2, 'You got currently '+str(player.levels)+' levels')
		popup.send(userid)
	else:
		tell(userid, 'You got 0 levels in the bank.')

def menu(userid):
	popupname = 'wcsbank_'+str(userid)
	popup = easymenu(popupname, '_popup_choice', menuHandler)
	popup.settitle('Select a player')

	popup.c_beginsep = None
	popup.c_pagesep = None

	for user in getPlayerList('#human'):
		popup.addoption(user.userid, user.name)

	popup.send(userid)

def menuHandler(userid, target, popupid):
	if exists('userid', target):
		popup = create('wcsbankselect_'+str(target))
		popup.addline('How many levels will you give '+str(getplayername(target)))
		popup.addline('->1. 1')
		popup.addline('->2. 5')
		popup.addline('->3. 10')
		popup.addline('->4. 25')
		popup.addline('->5. 100')
		popup.addline('->6. 250')
		popup.addline('->7. 1000')
		popup.addline('->8. 2500')
		popup.addline('->9. Back')
		popup.addline('0. Close')

		popup.menuselect = menuHandlerGetsHandled

		popup.send(userid)
	else:
		tell(userid, 'Unknown player')
		menu(userid)

def menuHandlerGetsHandled(userid, choice, popupid):
	if choice < 9:
		target = popupid.split('_')[1]
		if exists('userid', target):
			levels = [1,5,10,25,100,250,1000,2500][choice-1]
			getPlayer(target).levels += levels
			tell(userid, 'You gave '+str(levels)+' bank-levels to '+str(getplayername(target)))
			tell(target, 'You gained '+str(levels)+' bank-levels from an admin')
		else:
			tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 9:
		menu(userid)

def menuselect(userid, choice, popupid):
	if choice < 9:
		steamid = getplayersteamid(userid)
		paid   = [1,5,10,25,100,250,1000,2500][choice-1]
		player = getPlayer(userid)
		if paid <= player.levels:
			wgetPlayer(userid).race.addLevel(paid)
			player.levels -= paid
			tell(userid, 'You got '+str(player.levels)+' levels left in the bank.')
			if not player.levels:
				global tmp
				UserID = player.UserID
				del tmp[userid]
				database.execute("DELETE FROM Players WHERE UserID = ?", (UserID, ))
		else:
			tell(userid, 'Not enough bank-levels!')
			popup = find('wcsbanklevel')
			popup.modline(2, 'You got currently '+str(player.levels)+' levels')
			popup.send(userid)

def player_disconnect(ev):
	global tmp
	userid = int(ev['userid'])
	if userid in tmp:
		del tmp[userid]
