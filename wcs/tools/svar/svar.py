from es import ServerVar
from os.path import join
from wcs.wcs import logging, ini

def load():
	hmm = open(join(ini.path, 'tools', 'svar', 'var.txt'), 'r')
	lines = hmm.readlines()
	hmm.close()

	for line in lines:
		line = line.replace('\n', '').strip()
		if not line.startswith('//'):
			ServerVar(line).set(0)
			logging.log('svar: Information: Setting variable '+str(line)+' to 0', 3)
