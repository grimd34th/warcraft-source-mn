import es
import cheapcron
import time

from path import path

crons = cheapcron.CheapCronManager()

wcsfile = path(es.getAddonPath('wcs')).joinpath('data','players.sqlite')
path = path(es.getAddonPath('wcs')).joinpath('addons','backup','backups')

filenumber   = 0
timetodelete = 60*60*24*30 #30 days
				# s  m  h  d

def load():
	crons.daily(backup)

def backup():
	curtime = time.time()

	wcsfile.copy2(path.joinpath(time.strftime('%Y_%m_%d')+'-'+str(filenumber)+'.sqlite'))

	for x in path.listdir().copy():
		if x.ext == '.sqlite':
			name = x.basename().split('-')[0]
			filetime = x.atime

			if curtime-filetime >=  timetodelete:
				x.remove()

def es_map_start(ev):
	global filenumber

	filenumber += 1

	crons.check()