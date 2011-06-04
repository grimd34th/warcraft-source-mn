import es
import cmdlib
import gamethread
import popuplib
import playerlib
import usermsg
import weaponlib
from wcs import wcs

import os.path
import random



cfg = wcs.CfgManager('dm')

delayed = cfg.cvar('wcs_dm_delayed', 3, 'The seconds before the player are respawned')
disabled = cfg.cvar('wcs_dm_disabled', '', 'The disabled weapons will not show in the weapon list (use , to split them)')
spawnpoint = cfg.cvar('wcs_dm_spawnpoint', 1, 'Will respawn players on a random spawn point, read from a file (0 = OFF, 1 = ON)')

popups = {}
weapons = {}
spawnpoints = []

def load():
	p = popups['wcs_dm_main'] = popuplib.create('wcs_dm_main')
	p.addline('Weapons Options')
	p.addline('->1. New weapons')
	p.addline('->2. Same weapons')
	p.addline('->3. Same weapons every time')
	p.addline('->4. Random weapons')
	p.addline('->5. Random weapons every time')
	p.menuselect = main

	v = str(disabled).split(',')
	p = popups['wcs_dm_secondary'] = popuplib.easymenu('wcs_dm_secondary', '_popup_choice', secondary)
	p.settitle('Select a secondary weapon')
	for x in filter(lambda x: x not in v, weaponlib.getWeaponList('#secondary')):
		p.addoption(x, x)
	p.addoption(None, 'None')

	p = popups['wcs_dm_primary'] = popuplib.easymenu('wcs_dm_primary', '_popup_choice', primary)
	p.settitle('Select a primary weapon')
	for x in filter(lambda x: x not in v, weaponlib.getWeaponList('#primary')):
		p.addoption(x, x)
	p.addoption(None, 'None')

	cmdlib.registerClientCommand('wcs_dm_setspawnpoint', setSpawnPoint, '')
	cmdlib.registerSayCommand('guns', guns, '')

	es_map_start({})

def unload():
	cmdlib.unregisterClientCommand('wcs_dm_setspawnpoint')
	cmdlib.unregisterSayCommand('guns')

def player_death(ev):
	respawn(ev['userid'], int(delayed))

def player_spawn(ev):
	if int(ev['es_userteam']) >= 2:
		userid = int(ev['userid'])
		if userid in weapons and 'same' in weapons[userid] and weapons[userid]['same']:
			wcs.expand.removeWeapon(userid, 1)
			wcs.expand.removeWeapon(userid, 2)
			if weapons[userid]['primary']:
				wcs.expand.give(userid, weapons[userid]['primary'])
			if weapons[userid]['secondary']:
				wcs.expand.give(userid, weapons[userid]['secondary'])
		else:
			popups['wcs_dm_main'].send(userid)

		if int(ev['es_userdead']):
			respawn(userid, int(delayed))

def es_map_start(ev):
	global spawnpoints
	spawnpoints = []

	if os.path.isfile(os.path.join(wcs.ini.path, 'addons', 'dm', 'spawnpoints', str(es.ServerVar('eventscripts_currentmap'))+'.txt')):
		v = open(os.path.join(wcs.ini.path, 'addons', 'dm', 'spawnpoints', str(es.ServerVar('eventscripts_currentmap'))+'.txt'), 'r')
		spawnpoints = [x.strip() for x in v.readlines()]
		v.close()

def round_end(ev):
	gamethread.cancelDelayed('wcs_dm_respawn')



def main(userid, choice, popupid):
	userid = int(userid)

	if choice == 1:
		popups['wcs_dm_secondary'].send(userid)
	elif choice == 2 and userid in weapons:
		if userid in weapons:
			wcs.expand.removeWeapon(userid, 1)
			wcs.expand.removeWeapon(userid, 2)
			if weapons[userid]['primary']:
				wcs.expand.give(userid, weapons[userid]['primary'])
			if weapons[userid]['secondary']:
				wcs.expand.give(userid, weapons[userid]['secondary'])
		else:
			popuplib.send(popupid, userid)
	elif choice == 3:
		if userid in weapons:
			wcs.expand.removeWeapon(userid, 1)
			wcs.expand.removeWeapon(userid, 2)
			if weapons[userid]['primary']:
				wcs.expand.give(userid, weapons[userid]['primary'])
			if weapons[userid]['secondary']:
				wcs.expand.give(userid, weapons[userid]['secondary'])
			global weapons
			weapons[userid]['same'] = True
		else:
			popuplib.send(popupid, userid)
	elif choice == 4:
		wcs.expand.removeWeapon(userid, 1)
		wcs.expand.removeWeapon(userid, 2)
		wcs.expand.give(userid, random.choice(weaponlib.getWeaponList('#primary')))
		wcs.expand.give(userid, random.choice(weaponlib.getWeaponList('#secondary')))
	elif choice == 5:
		wcs.expand.removeWeapon(userid, 1)
		wcs.expand.removeWeapon(userid, 2)
		wcs.expand.give(userid, random.choice(weaponlib.getWeaponList('#primary')))
		wcs.expand.give(userid, random.choice(weaponlib.getWeaponList('#secondary')))
		global weapons
		weapons[userid]['same'] = True

def secondary(userid, choice, popupid):
	wcs.expand.removeWeapon(userid, 2)

	if choice:
		wcs.expand.give(userid, choice)

	if not int(userid) in weapons:
		weapons[int(userid)] = {'primary':None,'same':False}

	global weapons
	weapons[int(userid)]['secondary'] = choice

	popups['wcs_dm_primary'].send(userid)

def primary(userid, choice, popupid):
	wcs.expand.removeWeapon(userid, 1)

	if choice:
		wcs.expand.give(userid, choice)

	if not int(userid) in weapons:
		weapons[int(userid)] = {'secondary':None,'same':False}

	global weapons
	weapons[int(userid)]['primary'] = choice

def respawn(userid, time):
	if not time:
		wcs.expand.spawn(userid)

		if spawnpoint and spawnpoints:
			v = random.choice(spawnpoints).split(' ')
			es.entitysetvalue(playerlib.getPlayer(userid).index, 'origin', ' '.join(map(str, v[0:3])))
			es.entitysetvalue(playerlib.getPlayer(userid).index, 'angles', ' '.join(map(str, v[3:6])))

		#usermsg.hudhint(userid, wcs.strings('dm: respawned'))
	else:
		#usermsg.hudhint(userid, wcs.strings('dm: respawn in', {'time':time}))
		time -= 1
		gamethread.delayedname(1, 'wcs_dm_respawn', respawn, (userid, time))

def setSpawnPoint(userid, args):
	if wcs.admin.getPlayer(userid).hasFlag('dmadmin'):
		xyz = es.getplayerlocation(userid)
		pyr = es.entitygetvalue(playerlib.getPlayer(userid).index, 'angles').split(' ')

		v = open(os.path.join(wcs.ini.path, 'addons', 'dm', 'spawnpoints', str(es.ServerVar('eventscripts_currentmap'))+'.txt'), 'a')
		v.write(' '.join(map(str, [x for x in xyz]+[x for x in pyr]))+'\n')
		v.close()

		spawnpoints.append(' '.join(map(str, [x for x in xyz]+[x for x in pyr])))

		es.tell(userid, 'Successfully added the spawn point')

def guns(userid, args):
	userid = int(userid)

	global weapons
	if not userid in weapons:
		weapons[userid] = {'primary':None,'secondary':None}

	weapons[userid]['same'] = False

	popups['wcs_dm_main'].send(userid)

