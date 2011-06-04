from es import load as loll, unload as lolu
from os.path import join, isdir
from os import listdir
from wcs.wcs import ini




def load():
	for hello in listdir(join(ini.path, 'tools', 'abilitys')):
		if isdir(join(ini.path, 'tools', 'abilitys', hello)):
			loll('wcs/tools/abilitys/'+hello)

def unload():
	for hello in listdir(join(ini.path, 'tools', 'abilitys')):
		if isdir(join(ini.path, 'tools', 'abilitys', hello)):
			lolu('wcs/tools/abilitys/'+hello)
