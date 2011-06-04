import es
import os.path
import wcs


"""
"WCSgroups"
{
	"GROUP"
	{
		"KEY"		"SOMEVALUE1|SOMEVALUE2|SOMEVALUE3"
	}
}
"""


class Groups(object):
	def __contains__(self, item):
		if es.exists('key', 'WCSgroups', item):
			return True

		if es.exists('keyvalue', 'WCSgroups', item, 'KEY'):
			return True

		return False

	def __delitem__(self, item):
		if self.__contains__(item):
			es.keydelete('WCSgroups', item)

	def __getitem__(self, item):
		if self.__contains__(item):
			return str(es.keygetvalue('WCSgroups', item, 'KEY'))

		return ''

	def __setitem__(self, item, value):
		if not self.__contains__(item):
			es.keycreate('WCSgroups', item)

		if value[0:2] == '||' and len(value[2:]):
			value = value[2:]

		es.keysetvalue('WCSgroups', item, 'KEY', value)

	def load(self):
		if not os.path.isfile(os.path.join(wcs.wcs.ini.path, 'data', 'es_WCSgroups_db.txt')):
			es.keygroupcreate('WCSgroups')
			self.save()

		es.keygroupload('WCSgroups', '|wcs/data')

	def close(self):
		if es.exists('keygroup', 'WCSgroups'):
			es.keygroupdelete('WCSgroups')

	def save(self):
		es.keygroupsave('WCSgroups', '|wcs/data')
groups = Groups()

#Change it to sub-class list?
class getGroup(object):
	def __init__(self, group):
		self.group = str(group)

		if not self.group in groups:
			groups[self.group] = '|'

	def __contains__(self, item):
		return item in self.__list__()

	def __list__(self):
		return groups[self.group].split('|')

	def __iter__(self):
		for x in self.__list__():
			yield x

	def add(self, item):
		v = self.__list__()

		if item in v:
			return

		v.append(item)

		groups[self.group] = '|'.join(v)

	def has(self, item):
		return self.__contains__(item)

	def delete(self, item):
		v = self.__list__()

		if not item in v:
			return

		v.remove(item)

		groups[self.group] = '|'.join(v)
