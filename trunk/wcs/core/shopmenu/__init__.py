import es
from popuplib import easymenu, create, send
from playerlib import getPlayer
import wcs

import random

popups = []
items = {}
money = {}
maxitems = {}

'''def doCommand(userid, args):
	popup = easymenu('test'+str(userid), '_popup_choice', callBack)

	popup.settitle('Choose a category')

	popup.c_beginsep = None
	popup.c_pagesep = None

	allitems = wcs.wcs.ini.getItems
	for x in allitems.keys():
		popup.addoption(x, x)

	popup.send(userid)
	es.ServerVar('wcs_ppuser').set(userid)
	es.doblock("wcs/tools/pending/pending")

def popupHandler(userid, choice, popupid):
	doCommand1(userid, choice)

def doCommand1(userid, what):
	popup = easymenu('test'+str(userid), '_popup_choice', callBack1)

	popup.settitle('Choose an item')

	popup.c_beginsep = None
	popup.c_pagesep = None

	popup.c_exitformat  = '0. Back'
	popup.submenu(10, 'test'+str(userid))

	allitems = wcs.wcs.ini.getItems
	items = allitems[what]
	for x in items:
		if not x == 'desc':
			popup.addoption(what+'_'+x, items[x]['name'])

	popup.send(userid)
	es.ServerVar('wcs_ppuser').set(userid)
	es.doblock("wcs/tools/pending/pending")


def popupHandler1(userid, choice, popupid):
	allitems = wcs.wcs.ini.getItems
	place, item = choice.split('_')
	tell(userid, '#multi', 'You bought '+str(item))
	getPlayer(userid).cash -= int(allitems[place][item]['cost'])
	wcs.wcs.getPlayer(userid).giveItem(item)

callBack = popupHandler
callBack1 = popupHandler1'''


def doCommand(userid, args='shopmenu'):
	if args == 'shopmenu':
		args = 'shopmenu7'

	positionsearch = str(args.replace('shopmenu', '').strip())

	if len(positionsearch):
		if positionsearch.isdigit():
			positionsearch = int(positionsearch)
		else:
			positionsearch = 7
	else:
		positionsearch = 7

	allitems = wcs.wcs.itemdb.getSections()

	del allitems[:positionsearch - 7]
	del allitems[positionsearch:]

	if len(allitems):
		pname = 'shopmenu_%s_%s'%(userid, positionsearch)
		popups.append(pname)

		shopmenu = create(pname)

		shopmenu.addline('Choose a category')

		shopmenu.addline(' ')
		shopmenu.menuselect = callBack

		added = 0
		for item in allitems:
			if added < 7:
				added += 1
				shopmenu.addline('->'+str(added)+'. '+item)
			else:
				break

		while added < 8:
			shopmenu.addline(' ')
			added += 1
			shopmenu.submenu(added, pname)

		shopmenu.addline(' ')
		if positionsearch < 8:
			shopmenu.addline(' ')
			shopmenu.submenu(8, pname)
		else:
			shopmenu.addline('->8. Back')

		if len(allitems) < positionsearch:
			shopmenu.addline(' ')
			shopmenu.submenu(9, pname)
		else:
			shopmenu.addline('->9. Next')

		shopmenu.addline('0. Close')

		shopmenu.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")


def popupHandler(userid, choice, popupid):
	last_split  = popupid.split('_')
	last_search = int(last_split[2])

	if choice == 8:
		if last_search < 0:
			doCommand(userid, 'shopmenu7')

		elif last_search < 6:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)-7
			doCommand(userid, 'shopmenu%s'%newsearch)

	elif choice == 9:
		if last_search >= len(wcs.wcs.itemdb.getSections()):
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)+7
			doCommand(userid, 'shopmenu%s'%newsearch)

	elif choice < 8:
		#popup = 'shopmenu_%s_%s_7'%(userid, divmod(last_search, 7)[0]*7-(8-choice))
		popup = 'shopmenu_%s_%s_7'%(userid, choice)
		doCommand1(userid, popup)

def doCommand1(userid, args):
	try:
		args = args.split('_')
		choice = int(args[2])
		last_search = int(args[3])
		#shop_select = divmod(last_search, 7)[0]*7-(8-choice)
		shop_select = choice-1

		itemkeys = wcs.wcs.ini.getItems

		section = itemkeys.keys()[shop_select]
		values = itemkeys[section].keys()
		allvalues = list(values)

		allvalues.remove('desc')
		allvalues.remove('maxitems')
		del allvalues[:last_search - 7]
		del allvalues[last_search:]

		pname = 'shopmenu_%s_%s_%s'%(userid, choice, last_search)
		popups.append(pname)

		shopmenu = create(pname)

		shopmenu.addline('Choose an item')
		shopmenu.addline(itemkeys[section]['desc'])

		shopmenu.addline(' ')
		shopmenu.menuselect = callBack1

		added = 0
		for i, item in enumerate(allvalues):
			if added < 7:
				added += 1
				v = canBuy(userid, item)
				if not v:
					shopmenu.addline('->'+str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')
				else:
					shopmenu.addline(str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')
				'''elif v == 1:
					shopmenu.addline(str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')
				elif v == 2:
					shopmenu.addline(str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')
				elif v == 3:
					shopmenu.addline(str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')
				elif v == 4:
					shopmenu.addline(str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')
				elif v == 5:
					shopmenu.addline(str(added)+'. '+str(itemkeys[section][item]['name'])+' ($'+str(itemkeys[section][item]['cost'])+')')'''
			else:
				break

		while added < 7:
			shopmenu.addline(' ')
			added += 1
			shopmenu.submenu(added, pname)

		shopmenu.addline(' ')
		shopmenu.addline('->8. Back')

		values.remove('desc')
		values.remove('maxitems')

		if len(values) <= last_search:
			shopmenu.addline(' ')
			shopmenu.submenu(9, pname)
		else:
			shopmenu.addline('->9. Next')

		shopmenu.addline('0. Close')

		shopmenu.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")
	except IndexError:
		pass

def popupHandler1(userid, choice, popupid):
	userid = int(userid)
	last_split  = popupid.split('_')
	test = int(last_split[2])
	last_search = int(last_split[3])

	itemsa = wcs.wcs.ini.getItems
	section = itemsa.keys()[test-1]
	item = itemsa[section].keys()
	item.remove('desc')
	item.remove('maxitems')

	if choice in xrange(1, 8):
		if len(item) >= choice:
			item = item[divmod(last_search, 7)[0]*7-(8-choice)]
			addItem(userid, item, popupid=popupid)

	elif choice == 8:
		if last_search <= 0:
			doCommand(userid, 'shopmenu'+str(last_search))

		elif last_search < 8:
			doCommand(userid, 'shopmenu'+str(last_search))

		else:
			newsearch = int(last_search)-7
			doCommand1(userid, 'shopmenu_%s_%s_%s'%(userid, test, newsearch))

	elif choice == 9:
		if last_search >= len(item):
			send(popupid, userid)

		else:
			newsearch = int(last_search)+7
			doCommand1(userid, 'shopmenu_%s_%s_%s'%(userid, test, newsearch))


callBack = popupHandler
callBack1 = popupHandler1

def getPopups():
	return popups


def addItem(userid, item, pay=True, tell=True, popupid=None):
	section = wcs.wcs.itemdb.getSectionFromItem(item)
	itemsa = wcs.wcs.ini.getItems
	userid = int(userid)

	c = canBuy(userid, item, pay)

	if not c:
		if pay:
			if wcs.wcs.game == 'cstrike':
				getPlayer(userid).cash -= int(itemsa[section][item]['cost'])
			else:
				money[int(userid)] -= int(itemsa[section][item]['cost'])

		if tell:
			wcs.wcs.tell(userid, 'shopmenu: purchase', {'item':itemsa[section][item]['name']})

		if not userid in items:
			items[userid] = {}

		cfg = itemsa[section][item]['cfg']
		if not cfg in items[userid]:
			items[userid][cfg] = {}

		if not item in items[userid][cfg]:
			items[userid][cfg][item] = 0

		items[userid][cfg][item] += 1

		if not userid in maxitems:
			maxitems[userid] = {}

		if not section in maxitems[userid]:
			maxitems[userid][section] = 0

		maxitems[userid][section] += 1

		checkBuy(userid, item)

		wcs.wcs.events.Event('wcs_itembought').set({'userid':userid,'item':item,'cost':wcs.wcs.itemdb.getItem(item)['cost']}).fire()

	elif c == 1:
		if not popupid is None:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
		if tell:
			wcs.wcs.tell(userid, 'shopmenu: too many', {'item':itemsa[section][item]['name']})
	elif c == 2:
		if not popupid is None:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
		if tell:
			if wcs.wcs.game == 'cstrike':
				payment = getPlayer(userid).cash
			else:
				payment = money[int(userid)]
			wcs.wcs.tell(userid, 'shopmenu: not enough', {'cash':int(itemsa[section][item]['cost'])-payment,'item':itemsa[section][item]['name']})
	elif c == 3:
		if not popupid is None:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
		if tell:
			wcs.wcs.tell(userid, 'shopmenu: item restricted', {'item':itemsa[section][item]['name']})
	elif c == 4:
		if not popupid is None:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
		if tell:
			wcs.wcs.tell(userid, 'shopmenu: section item', {'item':itemsa[section][item]['name'], 'section':section})
	elif c == 5:
		if not popupid is None:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
		if tell:
			wcs.wcs.tell(userid, 'shopmenu: can\'t buy', {'item':itemsa[section][item]['name'],'status':['<death>','<alive>','<death or alive>'][int(itemsa[section][item]['dab'])]})
	elif c == 6:
		if not popupid is None:
			send(popupid, userid)
			iteminfo = wcs.wcs.itemdb.getItem(item)
			player = wcs.wcs.getPlayer(userid)
			diffience = int(iteminfo['level']) - int(player.race.level)
		if tell:
			wcs.wcs.tell(userid, 'shopmenu: nolevels', {'item':itemsa[section][item]['name'],'diffience':diffience})


def checkEvent(userid, event):
	userid = int(userid)
	if es.exists('userid', userid):
		if int(getPlayer(userid).team) > 1:
			if userid in items:
				if event in items[userid]:
					for item in items[userid][event]:
						v = items[userid][event][item]

						item, section = item, wcs.wcs.itemdb.getSectionFromItem(item)
						iteminfo = wcs.wcs.ini.getItems[section][item]

						es.ServerVar('wcs_userid').set(userid)
						es.ServerVar('wcs_dice').set(random.randint(0, 100))

						while v > 0:
							if (iteminfo['cfg'] == 'player_buy' or event == 'player_buy') and iteminfo['cmdbuy']:
								es.server.insertcmd(iteminfo['cmdbuy'])

							elif iteminfo['cmdactivate']:
								es.server.insertcmd(iteminfo['cmdactivate'])

							v -= 1

def checkBuy(userid, item):
	userid = int(userid)
	if es.exists('userid', userid):
		iteminfo = wcs.wcs.ini.getItems[wcs.wcs.itemdb.getSectionFromItem(item)][item]

		if int(not int(es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'))) == int(iteminfo['dab']) or int(iteminfo['dab']) == 2:
			es.ServerVar('wcs_userid').set(userid)
			es.ServerVar('wcs_dice').set(random.randint(0, 100))

			if iteminfo['cfg'] == 'player_buy' and iteminfo['cmdactivate']:
				es.server.insertcmd(iteminfo['cmdactivate'])
			elif iteminfo['cmdbuy']:
				es.server.insertcmd(iteminfo['cmdbuy'])

def canBuy(userid, item, pay=True):
	userid = int(userid)
	player = wcs.wcs.getPlayer(userid)
	level = player.race.level
	iteminfo = wcs.wcs.itemdb.getItem(item)

	if int(not int(es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'))) == int(iteminfo['dab']) or int(iteminfo['dab']) == 2:
		section = wcs.wcs.itemdb.getSectionFromItem(item)
		if not userid in maxitems:
			maxitems[userid] = {}

		if not section in maxitems[userid]:
			maxitems[userid][section] = 0

		if maxitems[userid][section] and int(wcs.wcs.itemdb[section]['maxitems']) <= maxitems[userid][section]:
			return 4
			
		if int(iteminfo['level']) and level < int(iteminfo['level']):
			return 6

		v = wcs.wcs.getPlayer(userid).race.racedb['restrictitem'].split('|')
		if (item in v) or ('ITEMS' in v):
			return 3

		cfg = iteminfo['cfg']
		if cfg in items[userid]:
			if item in items[userid][cfg]:
				if int(iteminfo['max']) and items[userid][cfg][item] >= int(iteminfo['max']):
					return 1
			
		if wcs.wcs.game == 'cstrike':
			payment = getPlayer(userid).cash
		else:
			payment = money[int(userid)]

		if payment >= int(iteminfo['cost']) or not pay:
			return 0
		return 2
	return 5
