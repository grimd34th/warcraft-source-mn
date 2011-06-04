import es
import cmdlib
import playerlib
from wcs import wcs

items = wcs.shopmenu.items
itemdb = wcs.itemdb
money = wcs.shopmenu.money
maxitems = wcs.shopmenu.maxitems



def player_death(ev):
	victim = int(ev['userid'])
	attacker = int(ev['attacker'])

	if attacker and victim:
		if not victim == attacker:
			if not ev['es_userteam'] == ev['es_attackerteam']:
				if int(wcs.cfgdata['allow_player_death']):
					wcs.shopmenu.checkEvent(victim, 'player_death')

				if int(wcs.cfgdata['allow_player_kill']):
					wcs.shopmenu.checkEvent(attacker, 'player_kill')

				if not wcs.game == 'cstrike':
					money[attacker] += 300

	if victim:
		_removeItems(victim, 1)
		if victim in maxitems:
			maxitems[victim].clear()

def player_hurt(ev):
	victim = int(ev['userid'])
	attacker = int(ev['attacker'])

	if attacker and victim and not ev['weapon'].lower() in ('point_hurt'):
		if not victim == attacker:
			if not ev['es_userteam'] == ev['es_attackerteam']:
				if int(wcs.cfgdata['allow_player_victim']):
					wcs.shopmenu.checkEvent(victim, 'player_victim')

				if int(wcs.cfgdata['allow_player_attacker']):
					wcs.shopmenu.checkEvent(attacker, 'player_attacker')

		if int(wcs.cfgdata['allow_player_hurt']):
			wcs.shopmenu.checkEvent(victim, 'player_hurt')
			wcs.shopmenu.checkEvent(attacker, 'player_hurt')

def player_spawn(ev):
	userid = int(ev['userid'])
	if userid:
		if int(wcs.cfgdata['allow_player_spawn']):
			wcs.shopmenu.checkEvent(userid, 'player_spawn')

def player_say(ev):
	text = ev['text'].lower()
	userid = ev['userid']

	if int(wcs.cfgdata['allow_player_say']):
		wcs.shopmenu.checkEvent(userid, 'player_say')

def round_end(ev):
	for x in money.copy():
		if not es.exists('userid', x):
			del money[x]

	if not wcs.game == 'cstrike':
		if ev['winner'] == '2':
			for user in playerlib.getUseridList('#t'):
				money[int(user)] += 3250
			for user in playerlib.getUseridList('#ct'):
				money[int(user)] += 1200
		elif ev['winner'] == '2':
			for user in playerlib.getUseridList('#t'):
				money[int(user)] += 1200
			for user in playerlib.getUseridList('#ct'):
				money[int(user)] += 3250

def player_activate(ev):
	userid = int(ev['userid'])
	if not userid in items:
		items[userid] = {}

	if not wcs.game == 'cstrike':
		money[userid] = 0

def player_disconnect(ev):
	userid = int(ev['userid'])
	if userid in items:
		del items[userid]

	if userid in maxitems:
		del maxitems[userid]

	if not wcs.game == 'cstrike':
		if userid in money:
			del money[userid]

def es_map_start(ev):
	items.clear()
	money.clear()
	maxitems.clear()



def load():
	for user in es.getUseridList():
		items[int(user)] = {}

	cmdlib.registerClientCommand('wcsbuyitem', register, '')
	cmdlib.registerSayCommand('wcsbuyitem', register, '')

	if not wcs.game == 'cstrike':
		cmdlib.registerClientCommand('credits', credits, '')
		cmdlib.registerSayCommand('credits', credits, '')

		for x in es.getUseridList():
			money[int(x)] = 0

def unload():
	items.clear()

	cmdlib.unregisterClientCommand('wcsbuyitem')
	cmdlib.unregisterSayCommand('wcsbuyitem')

	if not wcs.game == 'cstrike':
		cmdlib.unregisterClientCommand('credits')
		cmdlib.unregisterSayCommand('credits')

def register(userid, item):
	if len(item):
		item = ' '.join(map(str, item))
	else:
		item = None

	section = itemdb.getSectionFromItem(item)

	if section is not None and item in itemdb[section]:
		wcs.shopmenu.addItem(userid, item)

	else:
		es.tell(userid, '#default', 'fail')
		#wcs.tell(userid, 'shopmenu: unknown item', {'item':item})

def credits(userid, args):
	userid = int(userid)
	if not userid in money:
		wcs.tell(userid, 'shopmenu: credits', {'value':0})
		return

	wcs.tell(userid, 'shopmenu: credits', {'value':money[userid]})

def _removeItems(userid, value):
	if userid in items:
		for x in items[userid]:
			for q in items[userid][x].copy():
				item = wcs.itemdb.getItem(q)
				if int(item['duration']) == value:
					items[userid][x][q] = 0
