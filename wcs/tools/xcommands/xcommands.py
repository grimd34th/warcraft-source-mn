from es import exists, ServerVar
from cmdlib import registerServerCommand, unregisterServerCommand
from playerlib import getPlayer
from wcs.wcs import logging


def load():
	registerServerCommand('wcsx', register, 'Syntax: wcsx <get/set/math/call/create/split>')

def unload():
	unregisterServerCommand('wcsx')

def register(args):
	if len(args) >= 1:
		todo = str(args[0]).lower()

		if todo == 'get':
			if len(args) == 4:
				key = str(args[1])
				var = str(args[2])
				userid = str(args[3])

				if exists('userid', userid):
					player = getPlayer(userid)
					if hasattr(player, key):
						attr = getattr(player, key)

						if callable(attr):
							attr = attr()

						attr = _func(attr)

						ServerVar(var).set(attr)
					else:
						logging.log('xcommands: Error: '+key+' is not a valid wcsx get command!')
						logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))
				else:
					logging.log('xcommands: Information: Unknown userid: '+userid)
					logging.log('xcommands: Information: Args: wcsx '+' '.join(map(str, args)))
			else:
				logging.log('xcommands: Error: Syntax: wcsx get <key> <var> <userid>')
				logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

		elif todo == 'set':
			if len(args) >= 4:
				key = str(args[1])
				userid = str(args[2])

				if exists('userid', userid):
					player = getPlayer(userid)
					if hasattr(player, key):
						val = _func(args[3:])

						uhm = getattr(player, key)
						if hasattr(val, '__iter__') and not key in ('location'):
							val = val[0]

						if key in ('location') and not hasattr(val, '__iter__'):
							val = val.split(',')

						if callable(uhm):
							uhm(val)
						else:
							setattr(player, key, val)

					else:
						logging.log('xcommands: Error: '+key+' is not a valid wcsx set command!')
						logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))
				else:
					logging.log('xcommands: Information: Unknown userid: '+userid)
					logging.log('xcommands: Information: Args: wcsx '+' '.join(map(str, args)))
			else:
				logging.log('xcommands: Error: Syntax: wcsx set <key> <userid> <amount> <[amount1]> <[amount2]> <[amount3]>')
				logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

		elif todo == 'math':
			if len(args) == 5:
				key = str(args[1])
				userid = str(args[2])
				operator = str(args[3])
				amount = _convert(args[4])

				if exists('userid', userid):
					player = getPlayer(userid)
					if hasattr(player, key):
						keyv = getattr(player, key)
						if operator == '+':
							keyv += amount
						elif operator == '-':
							keyv -= amount
						elif operator == '=':
							keyv = amount
						else:
							logging.log('xcommands: Error: Unknown operator '+operator+'!')
							logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))
							return

						setattr(player, key, keyv)
					else:
						logging.log('xcommands: Error: '+key+' is not a valid wcsx math command!')
						logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))
				else:
					logging.log('xcommands: Information: Unknown userid: '+userid)
					logging.log('xcommands: Information: Args: wcsx '+' '.join(map(str, args)))
			else:
				logging.log('xcommands: Error: Syntax: wcsx math <key> <userid> <operator> <amount>')
				logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

		elif todo == 'call':
			if len(args) == 3:
				key = str(args[1])
				userid = str(args[2])

				if exists('userid', userid):
					player = getPlayer(userid)
					if hasattr(player, key):
						attr = getattr(player, key)
						if callable(attr):
							attr()
						else:
							logging.log('xcommands: Error: '+key+' is not callable!')
							logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

					else:
						logging.log('xcommands: Error: '+key+' is not a valid wcsx call command!')
						logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))
				else:
					logging.log('xcommands: Information: Unknown userid: '+userid)
					logging.log('xcommands: Information: Args: wcsx '+' '.join(map(str, args)))

			else:
				logging.log('xcommands: Error: Syntax: wcsx call <key> <userid>')
				logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

		elif todo == 'create':
			if len(args) >= 2:
				var = str(args[1])

				ServerVar(var).set(','.join(map(str, args[2:])))

			else:
				logging.log('xcommands: Error: Syntax: wcsx create <var> <value1> <[value2]> <[value3]>...')
				logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

		elif todo == 'split':
			if len(args) >= 3:
				value = str(args[1]).split(',')

				vars = args[2:]

				for x in xrange(0, len(vars)):
					ServerVar(vars[x]).set(value[x])

			else:
				logging.log('xcommands: Error: Syntax: wcsx split <values> <var1> <[var2]> <[var3]>...')
				logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

		else:
			logging.log('xcommands: Error: Syntax: wcsx <get/set/math/call/create/split>')
			logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))
	else:
		logging.log('xcommands: Error: Syntax: wcsx <get/set/math/call/create/split>')
		logging.log('xcommands: Information: Got: wcsx '+' '.join(map(str, args)))

def _func(args):
	if args and (str(args).isdigit() or len(str(args))):
		if not str(args).isdigit():
			if hasattr(args, '__iter__'):
				if hasattr(args[0], '__iter__'):
					if len(args[0]) == 1:
						return args[0][0]
					return ','.join(map(str, args[0]))
				return args[0]
	return args

def _convert(arg):
	if str(arg).isdigit():
		return int(arg)

	else:
		# If there's a better way to detect float, please, share.
		try:
			return float(arg)
		except ValueError:
			return str(arg)

	return arg
