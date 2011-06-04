import es
from playerlib import getPlayer, getUseridList, getPlayerList
from gamethread import delayed, delayedname, cancelDelayed, queue
from weaponlib import getWeaponList, getIndexList, getWeapon
from vecmath import Vector
from random import choice
import wcs

import os
_secure = True
if os.name == 'posix':
	_secure = False


try:
	import spe
except ImportError:
	spe = None

_selfmodule = __import__(__name__)

def spawn(userid, force=False):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			if force or es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
				if wcs.wcs.game == 'cstrike' and es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
					es.setplayerprop(user, 'CCSPlayer.m_iPlayerState', 0)
					es.setplayerprop(user, 'CBasePlayer.m_lifeState', 512)

				es.server.queuecmd('es_xspawnplayer '+str(user))
				#queue(es.spawnplayer, user) <- crash on Linux
				#es.spawnplayer(user) <- crash on Linux

def strip(userid):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.give(user, 'player_weaponstrip')
			es.fire(user, 'player_weaponstrip', 'strip')
			es.fire(user, 'player_weaponstrip', 'kill')

def drop(userid, weapon):
	if str(weapon).startswith('#'):
		weapon = getWeaponList(weapon)

	elif str(weapon).isdigit():
		weapon = filter(lambda wep: wep.slot == int(weapon), getWeaponList('#all'))

	elif not hasattr(weapon, '__iter__'):
		weapon = (weapon, )

	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			weplist = getPlayer(user).getWeaponList()

			for wep in weapon:
				if wep in weplist:
					#es.sexec(user, 'use '+wep+';drop ;use lastinv')
					es.server.queuecmd('es_xsexec '+str(user)+' "use '+wep+';drop;use lastinv"')

def push(userid, xm, ym=0, zm=0):
	if hasattr(xm, '__iter__'):
		xm = map(float, xm)
	else:
		xm = float(xm),float(ym),float(zm)

	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.setplayerprop(user, 'CBasePlayer.localdata.m_vecBaseVelocity', ','.join(map(str, xm)))

def pushto(userid, coord, force):
	if isinstance(coord, str):
		coord = coord.split(',')

	if hasattr(coord, '__iter__'):
		if not isinstance(coord, Vector):
			coord = Vector(coord)

	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			loca = Vector(es.getplayerlocation(user))
			coord -= loca
			coord = coord * float(force)

			es.setplayerprop(user, 'CBasePlayer.localdata.m_vecBaseVelocity', str(coord))

def damage(victim, damage, attacker=None, armor=False, weapon=None):
	if str(victim).startswith('#'):
		victim = getUseridList(victim)

	elif not hasattr(victim, '__iter__'):
		victim = (victim, )

	index = es.createentity('point_hurt')
	es.entitysetvalue(index, 'targetname', index)
	if not armor:
		es.entitysetvalue(index, 'damagetype', 32)
	if weapon:
		es.entitysetvalue(index, 'classname', weapon)

	for user in victim:
		if es.exists('userid', user):
			if damage == '#health':
				damage = es.getplayerprop(user, 'CBasePlayer.m_iHealth')

			es.entitysetvalue(index, 'damage', damage)

			pindex = getPlayer(user).index
			targetname = str(es.entitygetvalue(pindex, 'targetname'))
			es.entitysetvalue(pindex, 'targetname', user)
			es.fire(attacker, index, 'addoutput', 'damagetarget '+str(user))
			es.fire(attacker, index, 'hurt')
			es.fire(user, '!self', 'addoutput', 'targetname '+targetname)

	'''for user in victim:
		if es.exists('userid', user):
			if attacker is None:
				attacker = user

			es.entitysetvalue(index, 'targetname', index)
			if damage == '#health':
				damage = es.getplayerprop(user, 'CBasePlayer.m_iHealth')

			es.entitysetvalue(index, 'damage', str(damage))
			if not armor:
				es.entitysetvalue(index, 'damagetype', 32)
			if weapon:
				es.entitysetvalue(index, 'classname', weapon)

			pindex = getPlayer(user).index
			targetname = str(es.entitygetvalue(pindex, 'targetname'))
			es.entitysetvalue(pindex, 'targetname', user)
			es.fire(attacker, index, 'addoutput', 'damagetarget '+str(user))
			es.fire(attacker, index, 'hurt')
			es.fire(user, '!self', 'addoutput', 'targetname '+targetname)
			#es.fire(attacker, index, 'kill')'''

	user = es.getuserid()
	if user:
		es.fire(user, index, 'kill')
	else:
		es.remove(index)

_gravity = {}
def gravity(userid, value):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.fire(user, '!self', 'AddOutPut', 'gravity '+str(value))
			_gravity[int(user)] = float(value)


def _round_end(ev):
	_gravity.clear()
	cancelDelayed('_wcs_poison')
es.addons.registerForEvent(_selfmodule, 'round_end', _round_end)

def _player_jump(ev):
	user = int(ev['userid'])
	if user in _gravity:
		v = _gravity[user]

		if not float(v) == 1.0:
			es.fire(user, '!self', 'AddOutPut', 'gravity '+str(v))
es.addons.registerForEvent(_selfmodule, 'player_jump', _player_jump)

def removeWeapon(userid, weapon):
	if str(weapon).startswith('#'):
		weapon = getIndexList(weapon)

	elif str(weapon).isdigit():
		value = filter(lambda wep: wep.slot == int(weapon), getWeaponList('#all'))
		weapon = []
		for x in value:
			for q in es.createentitylist(x):
				weapon.append(q)

	elif not hasattr(weapon, '__iter__'):
		weapon = getIndexList(weapon)

	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			handle = es.getplayerhandle(user)

			for wep in weapon:
				if es.getindexprop(wep, 'CBaseEntity.m_hOwnerEntity') == handle:
					if spe:
						spe.removeEntityByIndex(wep)
					else:
						es.entitysetvalue(wep, 'TargetName', 'weaponremove')
						es.fire(user, 'weaponremove', 'Kill')

					es.cexec(user, 'lastinv')

def getViewEntity(userid):
	index = None

	###1 tick too late###
	#es.fire(userid, '!picker', 'AddOutPut', 'targetname __viewed_prop')

	###1 tick too late###
	#es.cexec(userid, "ent_setname __viewed_prop")

	###Crash on Linux but works perfectly
	#es.entsetname(userid, '__viewed_prop')

	###Doesn't work###
	#es.fire(userid, '!picker', 'TargetName', '__viewed_prop')

	###1 tick too late###
	#es.server.cmd('es_xentsetname '+str(userid)+' __viewed_prop')

	###Works on Windows, doesn't work on Linux nor crash###
	if _secure:
		es.entsetname(userid, '__viewed_prop')
	else:
		return None

	for i in es.createentitylist():
		if not es.entitygetvalue(i, 'TargetName') == '__viewed_prop':
			continue

		index = i
		es.entitysetvalue(i, 'TargetName', '')
		break
	
	return index

'''def getViewEntity(userid):
	index = {}
	v = es.createentityindexlist()

	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.entsetname(user, '__viewed_prop')

			for i in v:
				if not es.entitygetvalue(i, 'TargetName') == '__viewed_prop':
					continue

				index[int(user)] = i
				es.entitysetvalue(i, 'TargetName', '')
				#es.entitysetvalue(i, 'TargetName', tmp[i])
				break

		else:
			index[user] = None

	if len(index) == 1:
		return index[userid[0]]
	elif not index:
		return None

	return index'''

def getViewPlayer(userid):
	player = None
	index = getViewEntity(userid)
	if index:
		for p in getPlayerList():
			if p.index == index:
				player = int(p)
				break

	return player

'''def getViewPlayer(userid):
	player = None
	v = getViewEntity(userid)
	if v is None:
		return None

	for user in getPlayerList():
		if user.index == v:
			player = int(user)
			break

	return player'''

def keyHint(userid, text):
	if not len(text):
		return

	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	es.usermsg('create', 'keyhint', 'KeyHintText')
	es.usermsg('write', 'byte', 'keyhint', 1)
	es.usermsg('write', 'string', 'keyhint', text)

	for user in userid:
		if es.exists('userid', user):
			es.usermsg('send', 'keyhint', user)

	es.usermsg('delete', 'keyhint')

def give(userid, entity):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			#queue(es.give, (user, entity))
			es.server.queuecmd('es_xgive '+str(user)+' '+str(entity))
			#es.entcreate(user, entity)
			#es.entitysetvalue(int(es.ServerVar('eventscripts_lastgive')), 'origin', ' '.join(map(str, es.getplayerlocation(user))))

def fire(userid, time=0):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.fire(user, '!self', 'IgniteLifetime', time if time else 999)

def extinguish(userid):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.fire(user, '!self', 'IgniteLifetime', 0)

def drug(userid, time=0):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.cexec(user, 'r_screenoverlay effects/tp_eyefx/tp_eyefx')

			if time:
				delayed(time, es.cexec, (user, 'r_screenoverlay off'))

def _player_death(ev):
	userid = int(ev['userid'])
	es.cexec(userid, 'r_screenoverlay off')

es.addons.registerForEvent(_selfmodule, 'player_death', _player_death)

def drunk(userid, time=0, value=155):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			es.setplayerprop(user, 'CBasePlayer.m_iDefaultFOV', value)
			es.setplayerprop(user, 'CBasePlayer.m_iFOV', value)

			if time:
				delayed(time, es.setplayerprop, (user, 'CBasePlayer.m_iDefaultFOV', 90))
				delayed(time, es.setplayerprop, (user, 'CBasePlayer.m_iFOV', 90))

def _player_spawn(ev):
	userid = int(ev['userid'])
	es.cexec(userid, 'r_screenoverlay off')
	es.setplayerprop(userid, 'CBasePlayer.m_iDefaultFOV', 90)
	es.setplayerprop(userid, 'CBasePlayer.m_iFOV', 90)

es.addons.registerForEvent(_selfmodule, 'player_spawn', _player_spawn)

def dealPoison(userid, attacker, damage, time):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user) and not es.getplayerprop(user, 'CBasePlayer.pl.deadflag'):
			damage(user, damage, attacker)

	time -= 1
	if time:
		delayedname(1, '_wcs_poison', dealPoison, (userid, attacker, damage, time))

def changeTeam(userid, team):
	if str(userid).startswith('#'):
		userid = getUseridList(userid)

	elif not hasattr(userid, '__iter__'):
		userid = (userid, )

	for user in userid:
		if es.exists('userid', user):
			if team in ('2',2,'T','t'):
				es.setplayerprop(user, 'CCSPlayer.m_iClass', choice((1,2,3,4)))
				es.setplayerprop(user, 'CBaseEntity.m_iTeamNum', 2)
			elif team in ('3',3,'CT','ct'):
				es.setplayerprop(user, 'CCSPlayer.m_iClass', choice((5,6,7,8)))
				es.setplayerprop(user, 'CBaseEntity.m_iTeamNum', 3)
			elif team in ('1',1,'SPEC','spec'):
                                es.setplayerprop(user, 'CCSPlayer.m_iClass', 0)
				es.setplayerprop(user, 'CBaseEntity.m_iTeamNum', 1)
			else:
                                es.setplayerprop(user, 'CCSPlayer.m_iClass', 0)
				es.setplayerprop(user, 'CBaseEntity.m_iTeamNum', 0)
