import es
import cmdlib
import effectlib
import gamethread
import playerlib

import random

from wcs import wcs


moleDict = {}
delayed = set()

def load():
	cmdlib.registerServerCommand('wcs_mole_activate', moleActivate, 'A player becomes a mole')
	cmdlib.registerServerCommand('wcs_warden', warden, 'Warden, deals damage on nearby enemies')
	cmdlib.registerServerCommand('wcs_trap', trap, 'Trap, deals damage and slows on nearby enemies')
	cmdlib.registerServerCommand('wcs_heal', heal, 'Healing Ward, heals nearby friendly units')
	cmdlib.registerServerCommand('wcs_regeneration', regenerate, 'wcs_regeneration <userid> <amount> <time> <maxHP> <maxHeal> <radius> - Regenerate player for the current round')

	if not moleDict:
		make()

def unload():
	cmdlib.unregisterServerCommand('wcs_mole_activate')
	cmdlib.unregisterServerCommand('wcs_warden')
	cmdlib.unregisterServerCommand('wcs_trap')
	cmdlib.unregisterServerCommand('wcs_heal')
	cmdlib.unregisterServerCommand('wcs_regeneration')
	gamethread.cancelDelayed('wcs_mole')

	round_end({})

def moleActivate(args):
	if not len(args) == 1:
		wcs.logging.log('cmdskillspy: Error: Syntax: wcs_mole_activate <userid>')
		wcs.logging.log('cmdskillspy: Information: Got wcs_mole_activate '+' '.join(map(str, args)), 1)
		return

	userid = str(args[0])

	if es.exists('userid', userid):
		if not moleDict:
			make()

		#x,y,z = random.choice(moleDict[es.getplayerteam(userid)])
		index = playerlib.getPlayer(userid).index
		freeze = int(es.ServerVar('mp_freezetime'))
		es.server.queuecmd("es wcsgroup set ismole %s 1" % (userid))
		
		gamethread.delayedname(freeze, 'wcs_mole', wcs.tell, (userid, 'cmdskills: teleported mole'))
		gamethread.delayedname(freeze+3, 'wcs_mole', es.entitysetvalue, (index, 'origin', ' '.join(random.choice(moleDict[es.getplayerteam(userid)]))))

		#gamethread.delayed(freeze+3, es.setpos, (userid, x, y, z))
		model = ('player/ct_gign','player/ct_gsg9','player/ct_sas','player/ct_urban') if es.getplayerteam(userid) == 2 else ('player/t_arctic','player/t_phoenix','player/t_guerilla','player/t_leet')
		playerlib.getPlayer(userid).model = random.choice(model)

def warden(args):
	if not len(args) == 10:
		wcs.logging.log('cmdskillspy: Error: Syntax: wcs_warden <userid> <duration> <dmg> <radius> <target> <teagetn> <x> <y> <z> <wardenround>')
		wcs.logging.log('cmdskillspy: Information: Got wcs_warden '+' '.join(map(str, args)), 1)
		return

	userid = str(args[0])
	duration = int(args[1])
	dmg = int(float(args[2]))
	radius = int(args[3])
	target = str(args[4])
	targetn = str(args[5])
	x = float(args[6])
	y = float(args[7])
	z = float(args[8])
	round = int(args[9])

	if es.exists('userid', userid):
		r = 255 if es.getplayerteam(userid) == 2 else 0
		b = 255 if es.getplayerteam(userid) == 3 else 0

		for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
			x1,y1,z1 = es.getplayerlocation(user)
			immune = wcs.wcsgroup.getUser(user, 'swardinvul')
			if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius and not immune == 1:
				wcs.expand.damage(user, dmg, userid)
				wcs.tell(user, 'a_wardenhit')

				v = playerlib.getPlayer(user).speed
				playerlib.getPlayer(user).speed = 0.7

				gamethread.delayed(1, setSpeed, (user, v))

				effectlib.drawLine((x, y, z+30),(x1, y1, z1+30), model='sprites/lgtning.vmt', seconds=1, red=r, green=74, blue=b, brightness=200, width=10, endwidth=20)

		effectlib.drawCircle((x, y, z), radius, seconds=1, red=r, green=23, blue=b, brightness=200, width=10, endwidth=20)

		duration -= 1
		if duration:
			gamethread.delayedname(1, 'wcs_serpentward', warden, ([userid,duration,dmg,radius,target,targetn,x,y,z,round]))

def trap(args):
	if not len(args) == 10:
		wcs.logging.log('cmdskillspy: Error: Syntax: wcs_trap <userid> <duration> <dmg> <radius> <target> <teagetn> <x> <y> <z> <wardenround>')
		wcs.logging.log('cmdskillspy: Information: Got wcs_trap '+' '.join(map(str, args)), 1)
		return

	userid = str(args[0])
	duration = int(args[1])
	dmg = int(float(args[2]))
	radius = int(args[3])
	target = str(args[4])
	targetn = str(args[5])
	x = float(args[6])
	y = float(args[7])
	z = float(args[8])
	round = int(args[9])

	if es.exists('userid', userid):
		r = 204 if es.getplayerteam(userid) == 2 else 51
		b = 204 if es.getplayerteam(userid) == 3 else 51

		for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
			x1,y1,z1 = es.getplayerlocation(user)

			if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
				wcs.expand.damage(user, dmg, userid)
				wcs.tell(user, 'a_traphit')

				v = playerlib.getPlayer(user).speed
				playerlib.getPlayer(user).speed = 0.3

				gamethread.delayed(1, setSpeed, (user, v))

		duration -= 1
		if duration:
			gamethread.delayedname(1, 'wcs_trapward', trap, ([userid,duration,dmg,radius,target,targetn,x,y,z,round]))

def heal(args):
	if not len(args) == 10:
		wcs.logging.log('cmdskillspy: Error: Syntax: wcs_heal <userid> <duration> <dmg> <radius> <target> <teagetn> <x> <y> <z> <wardenround>')
		wcs.logging.log('cmdskillspy: Information: Got wcs_heal '+' '.join(map(str, args)), 1)
		return

	userid = str(args[0])
	duration = int(args[1])
	dmg = int(float(args[2]))
	radius = int(args[3])
	target = str(args[4])
	targetn = str(args[5])
	x = float(args[6])
	y = float(args[7])
	z = float(args[8])
	round = int(args[9])

	if es.exists('userid', userid):
		r = 204 if es.getplayerteam(userid) == 2 else 51
		b = 204 if es.getplayerteam(userid) == 3 else 51

		for user in playerlib.getUseridList('#alive,#'+['t','ct'][es.getplayerteam(userid)-2]):
			x1,y1,z1 = es.getplayerlocation(user)

			if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
				wcs.tell(user, 'a_healhit')

				playerlib.getPlayer(user).health += 3

		duration -= 1
		if duration:
			gamethread.delayedname(1, 'wcs_healward', heal, ([userid,duration,dmg,radius,target,targetn,x,y,z,round]))

def regenerate(args):
	if not len(args) == 6:
		wcs.logging.log('cmdskillspy: Error: Syntax: wcs_regeneration <userid> <amount> <time> <maxHP> <maxHeal> <radius>')
		wcs.logging.log('cmdskillspy: Information: Got wcs_regeneration '+' '.join(map(str, args)), 1)
		return

	userid = str(args[0])
	amount = int(args[1])
	time = float(args[2])
	maxhp = int(args[3])
	maxheal = int(args[4])
	radius = int(args[5])

	if es.exists('userid', userid) and not es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
		if time or time == -1:
			if radius:
				x,y,z = es.getplayerlocation(userid)

				for user in playerlib.getPlayerList('#alive,#'+['t','ct'][es.getplayerteam(userid)-2]):
					x1,y1,z1 = user.location

					if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
						user.health += amount
						if maxheal and not maxheal == -1 and maxheal < user.health:
							user.health = maxheal

						wcs.tell(user, 'a_regenhit')

			else:
				v = playerlib.getPlayer(userid)
				v.health += amount
				if maxheal and not maxheal == -1 and maxheal < v.health:
					v.health = maxheal

				wcs.tell(userid, 'a_regenhit')

		delayed.add('wcs_regeneration'+userid)
		gamethread.delayedname(time, 'wcs_regeneration'+userid, regenerate, ([userid,amount,time,maxhp,maxheal,radius]))

def round_end(ev):
	gamethread.cancelDelayed('wcs_serpentward')
	gamethread.cancelDelayed('wcs_trapward')
	gamethread.cancelDelayed('wcs_healward')
	for x in delayed:
		gamethread.cancelDelayed(x)

	delayed.clear()

def es_map_start(ev):
	moleDict.clear()

	make()

def make():
	moleDict[2] = []
	moleDict[3] = []

	for x in es.createentitylist('info_player_counterterrorist'):
		moleDict[2].append(es.entitygetvalue(x, 'origin').split(' '))

	for x in es.createentitylist('info_player_terrorist'):
		moleDict[3].append(es.entitygetvalue(x, 'origin').split(' '))

def setSpeed(userid, speed):
	if es.exists('userid', userid):
		playerlib.getPlayer(userid).speed = speed


def player_death(ev):
	userid = ev['userid']
	es.server.queuecmd("es wcsgroup set ismole %s 1" % (userid))


