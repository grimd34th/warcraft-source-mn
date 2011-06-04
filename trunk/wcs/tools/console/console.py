import es
from es import ServerVar, exists
from playerlib import getPlayer as gP
from cmdlib import registerServerCommand, unregisterServerCommand
from wcs.wcs import logging, getPlayer, _getRace, racedb, wcsgroup, cancel
 
from time import time
 
def load():
	registerServerCommand('wcs_givexp', givexpRegister, 'Syntax: wcs_givexp <userid> <amount> <[reason]>')
	registerServerCommand('wcs_givelevel', givelevelRegister, 'Syntax: wcs_givelevel <userid> <amount>')
	registerServerCommand('wcs_getinfo', getInfoRegister, 'Syntax: wcs_getinfo <userid> <var> <info> <race/player/racename>')
	registerServerCommand('wcs_decimal', decimalRegister, 'Syntax: wcs_decimal <var> <amount>')
	registerServerCommand('wcs_cancelulti', ultiRegister, 'Syntax: wcs_cancelulti <userid>')
	registerServerCommand('wcs_color', colorRegister, 'Syntax: wcs_color <userid> <red> <green> <blue> <alpha> <[weapon]>')
	registerServerCommand('wcs_getindex', indexRegister, 'Syntax: wcs_getindex <var> <userid>')
	registerServerCommand('wcs_raceinfo', raceInfoRegister, 'Syntax: wcs_raceinfo <var> <race> <key>')
 
def unload():
	unregisterServerCommand('wcs_givexp')
	unregisterServerCommand('wcs_givelevel')
	unregisterServerCommand('wcs_getinfo')
	unregisterServerCommand('wcs_decimal')
	unregisterServerCommand('wcs_cancelulti')
	unregisterServerCommand('wcs_color')
	unregisterServerCommand('wcs_getindex')
	unregisterServerCommand('wcs_raceinfo')
 
def givexpRegister(args):
	if len(args) >= 2:
		userid = str(args[0])
		amount = int(args[1])
 
		if not exists('userid', userid):
			logging.log('console: Information: Unknown userid: '+userid)
			logging.log('console: Information: Args: wcs_givexp '+' '.join(map(str, args)))
			return
 
		if not amount:
			return
 
		reason = ''
		if len(args) >= 3:
			reason = str(args[2])
			if reason.isdigit():
				reason = ''
 
		getPlayer(userid).giveXp(amount, reason)
	else:
		logging.log('console: Error: Syntax: wcs_givexp <userid> <amount> <[reason]>')
		logging.log('console: Information: Got: wcs_givexp '+' '.join(map(str, args)), 1)
 
def givelevelRegister(args):
	if len(args) >= 2:
		userid = str(args[0])
		amount = int(args[1])
 
		if not exists('userid', userid):
			logging.log('console: Information: Unknown userid: '+userid)
			logging.log('console: Information: Args: wcs_givelevel '+' '.join(map(str, args)))
			return
 
		if not amount:
			return
 
		getPlayer(userid).giveLevel(amount)
	else:
		logging.log('console: Error: Syntax: wcs_givelevel <userid> <amount>')
		logging.log('console: Information: Got: wcs_givelevel '+' '.join(map(str, args)), 1)
 
def getInfoRegister(args):
	if len(args) == 4:
		userid = str(args[0])
		var = str(args[1])
		info = str(args[2])
		where = str(args[3])
 
		if not exists('userid', userid):
			es.ServerVar(var).set(0)
			logging.log('console: Information: Unknown userid: '+userid)
			logging.log('console: Information: Args: wcs_getinfo '+' '.join(map(str, args)))
			return
 
		player = getPlayer(userid)
 
		if where == 'race':
			if hasattr(player.race, info):
				returned = getattr(player.race, info)
				ServerVar(var).set(returned)
 
			else:
				logging.log('console: Error: Unknown info: '+info)
				logging.log('console: Information: Got: wcs_getinfo '+' '.join(map(str, args)), 1)
 
		elif where == 'player':
			if hasattr(player.player, info):
				returned = getattr(player.player, info)
				ServerVar(var).set(returned)
 
			else:
				logging.log('console: Error: Unknown info: '+info)
				logging.log('console: Information: Got: wcs_getinfo '+' '.join(map(str, args)), 1)
 
		else:
			if not where in racedb:
				logging.log('console: Error: Unknown info: '+info)
				logging.log('console: Information: Got: wcs_getinfo '+' '.join(map(str, args)), 1)
				return
 
			v = _getRace(player.player.UserID, info, userid)
			if hasattr(v, info):
				returned = getattr(v, info)
				ServerVar(var).set(returned)
 
			else:
				logging.log('console: Error: Unknown info: '+info)
				logging.log('console: Information: Got: wcs_getinfo '+' '.join(map(str, args)), 1)
 
	else:
		logging.log('console: Error: Syntax: wcs_getinfo <userid> <var> <info> <race/player>')
		logging.log('console: Information: Got: wcs_getinfo '+' '.join(map(str, args)), 1)
 
def decimalRegister(args):
	if len(args) == 2:
		var = str(args[0])
		amount = str(args[1])
 
		'''number = str(number)
		if not '.' in number and number.isdigit():
			return int(number)
		i,v = number.split('.')
		v = v[:val]
		if val:
			return float(i+('.' if v else '')+v)
		return int(i)'''
 
		ServerVar(var).set(round(float(amount)))
 
	else:
		logging.log('console: Error: Syntax: wcs_decimal <var> <amount>')
		logging.log('console: Information: Got: wcs_decimal '+' '.join(map(str, args)), 1)
 
def ultiRegister(args):
	if len(args) == 1:
		userid = str(args[0])
 
		if not exists('userid', userid):
			logging.log('console: Information: Unknown userid: '+userid)
			logging.log('console: Information: Args: wcs_cancelulti '+' '.join(map(str, args)))
			return
 
		cancel(userid, 'player_ultimate')
		#wcsgroup.setUser(userid, 'player_ultimate_cooldown', wcsgroup.getUser(userid, 'player_ultimate_pre_cooldown'))
 
	else:
		logging.log('console: Error: Syntax: wcs_cancelulti <userid>')
		logging.log('console: Information: Got: wcs_cancelulti '+' '.join(map(str, args)), 1)
 
def colorRegister(args):
	if len(args) >= 5:
		userid = str(args[0])
		red = int(float(args[1]))
		green = int(float(args[2]))
		blue = int(float(args[3]))
		alpha = int(float(args[4]))
 
		player = gP(userid)
 
		player.color = (red, green, blue, alpha)
 
		if len(args) == 6 and str(args[5]).isdigit() and int(args[5]):
			if player.getWeaponList():
				player.weaponcolor = (red, green, blue, alpha)
 
	else:
		logging.log('console: Error: Syntax: wcs_color <userid> <red> <green> <blue> <alpha> <[weapon]>')
		logging.log('console: Information: Got: wcs_color '+' '.join(map(str, args)), 1)
 
def indexRegister(args):
	if len(args) == 2:
		var, userid = map(str, args)
 
		if exists('userid', userid):
			ServerVar(var).set(gP(userid).index)
		else:
			ServerVar(var).set(0)
 
	else:
		logging.log('console: Error: Syntax: wcs_getindex <var> <userid>')
		logging.log('console: Information: Got: wcs_getindex '+' '.join(map(str, args)), 1)
 
def raceInfoRegister(args):
        if len(args) <= 3:
                var, race, key = map(str, args[:3])
 
                if not race in racedb:
                        logging.log('console: Error: Unknown race: '+race)
                        logging.log('console: Information: Got: wcs_raceinfo '+' '.join(map(str, args)), 1)
                        return
 
                if not key in racedb.getRace(race):
                        logging.log('console: Error: Unknown key: '+key)
                        logging.log('console: Information: Got: wcs_raceinfo '+' '.join(map(str, args)), 1)
                        return
 
                if key.startswith('skill'):
                        if not len(args) == 4:
                                logging.log('console: Error: Syntax: wcs_raceinfo <var> <race> [<skill>] <key>')
                                logging.log('console: Information: Got: wcs_raceinfo '+' '.join(map(str, args)), 1)
                                return
 
                        nkey = args[4]
 
                        if not nkey in racedb.getRace(race)[key]:
                                logging.log('console: Error: Unknown key: '+nkey)
                                logging.log('console: Information: Got: wcs_raceinfo '+' '.join(map(str, args)), 1)
                                return
 
                        es.ServerVar(var).set(racedb.getRace(race)[key][nkey])
                        return
 
                es.ServerVar(var).set(racedb.getRace(race)[key])
 
        else:
                logging.log('console: Error: Syntax: wcs_raceinfo <var> <race> [<skill>] <key>')
                logging.log('console: Information: Got: wcs_raceinfo '+' '.join(map(str, args)), 1)