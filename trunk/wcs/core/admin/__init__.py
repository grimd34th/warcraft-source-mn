import es
import os.path
import wcs


"""
"WCSadmins"
{
	"STEAMID"
	{
		"FLAG"		"1/0"
	}
}
"""

class Admins(object):
	def __contains__(self, item):
		if es.exists('key', 'WCSadmins', item):
			return True

		if len(item) == 2:
			if es.exists('keyvalue', 'WCSadmins', item[0], item[1]):
				return True

		return False

	def __delitem__(self, item):
		if exists('key', 'WCSadmins', item):
			es.keydelete('WCSadmins', item)

	def __getitem__(self, item):
		if es.exists('keyvalue', 'WCSadmins', item[0], item[1]):
			return int(es.keygetvalue('WCSadmins', item[0], item[1]))

		return 0

	def __setitem__(self, item, value):
		if len(item) == 1:
			es.keycreate('WCSadmins', item)
		else:
			if not es.exists('key', 'WCSadmins', item[0]):
				es.keycreate('WCSadmins', item[0])

			es.keysetvalue('WCSadmins', item[0], item[1], value)

	def load(self):
		if not os.path.isfile(os.path.join(wcs.wcs.ini.path, 'data', 'es_WCSadmins_db.txt')):
			es.keygroupcreate('WCSadmins')
			self.save()

		es.keygroupload('WCSadmins', '|wcs/data')

	def close(self):
		if es.exists('keygroup', 'WCSadmins'):
			es.keygroupdelete('WCSadmins')

	def save(self):
		es.keygroupsave('WCSadmins', '|wcs/data')
admins = Admins()

class getPlayer(object):
	def __init__(self, userid):
		self.userid = str(userid)
		self.steamid = es.getplayersteamid(self.userid)

		if not self.steamid:
			raise TypeError, 'Unknown userid: '+self.userid

	def __int__(self):
		return int(self.userid)

	def __str__(self):
		return self.userid

	def __contains__(self, item):
		return (self.steamid, item) in admins

	def hasFlag(self, flag):
		if not self.steamid in admins:
			return False

		if not self.__contains__(flag):
			return False

		return bool(admins[(self.steamid, flag)])

	def setFlag(self, flag, value=1):
		admins[(self.steamid, flag)] = value
