from es import load as loll, unload as lolu
from os.path import join, isdir
from os import listdir
from wcs.wcs import ini

file = open(join(ini.path, 'config', 'addons.cfg'), 'r')
lines = file.readlines()
file.close

lines = filter(lambda x: not x.strip().startswith('//'), lines)


def load():
	for hello in lines:
		hello = hello.replace('\n', '').replace('\r', '')
		if hello:
			if isdir(join(ini.path, 'addons', hello)):
				loll('wcs/addons/'+hello)

def unload():
	for hello in lines:
		hello = hello.replace('\n', '').replace('\r', '')
		if hello:
			if isdir(join(ini.path, 'addons', hello)):
				lolu('wcs/addons/'+hello)
