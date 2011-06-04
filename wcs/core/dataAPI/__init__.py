from es import getAddonPath
from os.path import isfile, join
from cPickle import load, dump



class DB(object):
	def __init__(self, name):
		self.path = join(getAddonPath('wcs'), 'data', name+'.db')
		self.data = {}

	def __contains__(self, item):
		return item in self.data

	def __iter__(self):
		for x in self.data:
			yield x

	def __list__(self):
		return self.data.keys()

	def __dict__(self):
		return self.data

	def __delitem__(self, item):
		if self.item in self.data:
			del self.data[item]

	def __getitem__(self, item):
 		return self.data[item]

	def __setitem__(self, item, value):
		self.data[item] = value

	def load(self):
		if isfile(self.path):
			str_path = open(self.path)
			self.data = load(str_path)
			str_path.close()

	def save(self):
		str_path = open(self.path, 'w')
		dump(self.data, str_path)
		str_path.close()
