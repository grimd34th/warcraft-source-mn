from es import ServerVar, getAddonPath, dbgmsg
from os.path import join, isdir
from os import mkdir
from time import strftime


def log(text, level=0):
	if int(ServerVar('wcs_log')) >= level:
		path = join(getAddonPath('wcs'), 'logs')
		if not isdir(path):
			mkdir(path)

		path = join(path, strftime('%m%d.log'))

		file = open(path, 'a+')

		file.write(strftime('L %m/%d/%Y - %H:%M:%S: ')+str(text)+'\n')
		file.close()

		dbgmsg(0, str(text))
