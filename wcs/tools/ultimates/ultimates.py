from es import load as loll, unload as lolu
from os.path import join, isdir
from os import listdir
from wcs.wcs import ini




def load():
	for hello in listdir(join(ini.path, 'tools', 'ultimates')):
		if isdir(join(ini.path, 'tools', 'ultimates', hello)):
			loll('wcs/tools/ultimates/'+hello)

def unload():
	for hello in listdir(join(ini.path, 'tools', 'ultimates')):
		if isdir(join(ini.path, 'tools', 'ultimates', hello)):
			lolu('wcs/tools/ultimates/'+hello)
