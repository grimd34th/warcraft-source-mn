import es
import keyvalues
import path
import os.path

class key(object):
	def __init__(self, filename, keygroup='PLAYERS'):
		self.filename = str(filename)
		self.keygroup = keygroup
		if es.exists('keygroup', self.filename):
			es.keygroupdelete(self.filename)
		self.data = keyvalues.KeyValues(name=self.keygroup)
		self.path = os.path.join(es.getAddonPath('wcs'), 'data', 'es_'+self.filename+'_db.txt')

	def __del__(self):
		self.data.__del__()

	def __contains__(self, item):
		return self.data.__contains__(item)

	def __delitem__(self, item):
		self.data.__delitem__(item)

	def __getitem__(self, item):
		return self.data.__getitem__(item)

	def __setitem__(self, item, value):
		if value == keyvalues.KeyValues:
			self.data[item] = keyvalues.KeyValues(name=item)
		else:
			self.data.__setitem__(item, value)

	def __iter__(self):
		return self.data.__iter__()

	def load(self):
		self.data.load(self.path)

	def save(self):
		self.data.save(self.path)

	def new(self):
		return keyvalues.KeyValues
