from path import path
from sqlite3 import dbapi2 as sqlite
import wcs

class SQLiteAPI:
	def __init__(self, name):
		self.name = str(name)
		self.path = path(wcs.wcs.ini.path).joinpath('data').joinpath(self.name if self.name.endswith('.sqlite') else self.name+'.sqlite')

	def __del__(self):
		self.save()
		self.close()

	def connect(self):
		self.connection   = sqlite.connect(self.path)
		self.cursor       = self.connection.cursor()

		self.connection.text_factory = str

		self.create()

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

	def create(self):
		pass
