from es import exists, getplayerlocation, getplayerhandle, ServerVar
from cmdlib import registerServerCommand, unregisterServerCommand
from wcs.wcs import logging, expand, effect, friendlyexplosion

def load():
	registerServerCommand('wcs', register, 'wcs <damage/explode/spawn/strip/drop/push/pushto/gravity/removeweapon/getviewplayer/getviewentity/keyhint/give/fire/extinguish/drug/drunk/poison> <userid>')

def unload():
	unregisterServerCommand('wcs')

def register(args):
	if len(args) >= 2:
		todo = str(args[0]).lower()
		userid = str(args[1])

		if exists('userid', userid):
			if todo == 'damage':
				if len(args) >= 4:
					v,q,w = int(args[2]) if int(args[2]) else None, int(args[4]) if len(args) >= 5 else False, str(args[5]) if len(args) == 6 else None
					expand.damage(userid, str(args[3]), v, q, w)
					#server.insertcmd('damage %s %s 32 %s'%(userid, int(float(args[3])), str(args[2])))
				else:
					logging.log('commands: Error: Syntax: wcs damage <userid> <attacker> <amount> <[armor]> <[weapon]>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'explode':
				if len(args) == 5:
					if friendlyexplosion:
						effect.effect.Explosion(getplayerlocation(args[2]), IMagniTude=int(float(args[3])), IRadiusOverride=int(float(args[4])), HOwner=getplayerhandle(userid))
					else:
						magnitude = round(float(args[3]) * float(args[4]) / 150)
						#server.damage(args[2], magnitude, 32, userid)
						expand.damage(args[2], magnitude, userid)
						#player.damage(magnitude, 32, args[2])
						#server.insertcmd('damage %s %s 32 %s'%(args[2], magnitude, userid))
				else:
					logging.log('commands: Error: Syntax: wcs explode <userid> <targetid> <magnitude> <radius>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'spawn':
				if len(args) in (2,3):
					expand.spawn(userid, int(args[2]) if len(args) == 3 else False)
				else:
					logging.log('commands: Error: Syntax: wcs spawn <userid> <[force]>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'strip':
				if len(args) == 2:
					expand.strip(userid)
				else:
					logging.log('commands: Error: Syntax: wcs strip <userid>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'drop':
				if len(args) == 3:
					expand.drop(userid, args[2])
				else:
					logging.log('commands: Error: Syntax: wcs drop <userid> <weapon/slot/tag>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'push':
				if len(args) >= 3:
					expand.push(userid, args[2], args[3] if len(args) >= 4 else 0, args[4] if len(args) == 5 else 0)
				else:
					logging.log('commands: Error: Syntax: wcs push <userid> <x force> <[y force]> <[z force]>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'pushto':
				if len(args) == 4:
					expand.pushto(userid, args[2], args[3])
				else:
					logging.log('commands: Error: Syntax: wcs pushto <userid> <x,y,z> <force>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'gravity':
				if len(args) == 3:
					expand.gravity(userid, args[2])
				else:
					logging.log('commands: Error: Syntax: wcs gravity <userid> <value>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'removeweapon':
				if len(args) == 3:
					expand.removeWeapon(userid, args[2])
				else:
					logging.log('commands: Error: Syntax: wcs removeweapon <userid> <weapon/slot/tag>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'getviewplayer':
				if len(args) == 3:
					v = expand.getViewPlayer(userid)
					ServerVar(args[2]).set(v if v is not None else 0)
				else:
					logging.log('commands: Error: Syntax: wcs getviewplayer <userid> <var>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'getviewentity':
				if len(args) == 3:
					v = expand.getViewEntity(userid)
					ServerVar(args[2]).set(v if v is not None else 0)
				else:
					logging.log('commands: Error: Syntax: wcs getviewentity <userid> <var>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'keyhint':
				if len(args) >= 3:
					expand.keyHint(userid, ' '.join(map(str, args[3:])))
				else:
					logging.log('commands: Error: Syntax: wcs keyhint <userid> <text...>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'give':
				if len(args) == 3:
					expand.give(userid, args[2])
				else:
					logging.log('commands: Error: Syntax: wcs give <userid> <entity>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'fire':
				if len(args) >= 2:
					expand.fire(userid, args[2] if len(args) == 3 else 0)
				else:
					logging.log('commands: Error: Syntax: wcs fire <userid> <[time]>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'extinguish':
				if len(args) == 2:
					expand.extinguish(userid)
				else:
					logging.log('commands: Error: Syntax: wcs extinguish <userid>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'drug':
				if len(args) >= 2:
					expand.drug(userid, float(args[2]) if len(args) >= 3 else 0)
				else:
					logging.log('commands: Error: Syntax: wcs drug <userid> <[time]>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'drunk':
				if len(args) >= 2:
					expand.drunk(userid, float(args[2]) if len(args) >= 3 else 0, int(args[3]) if len(args) == 4 else 155)
				else:
					logging.log('commands: Error: Syntax: wcs drunk <userid> <[time]> <[value]>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'poison':
				if len(args) == 5:
					expand.dealPoison(userid, int(float(args[3])), str(args[2]), int(args[4]))
				else:
					logging.log('commands: Error: Syntax: wcs poison <userid> <attacker> <amount> <time>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			elif todo == 'changeteam':
				if len(args) == 3:
					expand.changeTeam(userid, str(args[2]))
				else:
					logging.log('commands: Error: Syntax: wcs changeteam <userid> <team>')
					logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

			else:
				logging.log('commands: Error: Syntax: wcs <damage/explode/spawn/strip/drop/push/pushto/gravity/removeweapon/getviewplayer/getviewentity/keyhint/give/fire/extinguish/drug/drunk/poison> <userid>')
				logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)

		else:
			logging.log('commands: Information: Unknown userid: '+userid)
			logging.log('commands: Information: Args: wcs '+' '.join(map(str, args)))
	else:
		logging.log('commands: Error: Syntax: wcs <damage/explode/spawn/strip/drop/push/pushto/gravity/removeweapon/getviewplayer/getviewentity/keyhint/give/fire/extinguish/drug/drunk/poison> <userid>')
		logging.log('commands: Information: Got: wcs '+' '.join(map(str, args)), 1)
