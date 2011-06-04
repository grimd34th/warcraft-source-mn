import es
from popuplib import easymenu, create, send
from playerlib import getPlayer
import wcs

popups = []



def doCommand(userid, args='shopinfo7'):
	if args == 'shopinfo':
		args = 'shopinfo7'

	positionsearch = str(args.replace('shopinfo', '').strip())

	if len(positionsearch):
		if positionsearch.isdigit():
			positionsearch = int(positionsearch)
		else:
			positionsearch = 0
	else:
		positionsearch = 0

	allitems = wcs.wcs.ini.getItems.keys()

	del allitems[:positionsearch - 7]
	del allitems[positionsearch:]

	if len(allitems):
		pname = 'shopinfo_%s_%s'%(userid, positionsearch)
		popups.append(pname)

		shopinfo = create(pname)

		shopinfo.addline('Choose a category')

		shopinfo.addline(' ')
		shopinfo.menuselect = callBack

		added = 0
		for item in allitems:
			if added < 7:
				added += 1
				shopinfo.addline('->'+str(added)+'. '+item)
			else:
				break

		while added < 8:
			shopinfo.addline(' ')
			added += 1
			shopinfo.submenu(added, pname)

		shopinfo.addline(' ')
		if positionsearch < 8:
			shopinfo.addline(' ')
			shopinfo.submenu(8, pname)
		else:
			shopinfo.addline('->8. Back')

		if len(allitems) < positionsearch:
			shopinfo.addline(' ')
			shopinfo.submenu(9, pname)
		else:
			shopinfo.addline('->9. Next')

		shopinfo.addline('0. Close')

		shopinfo.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")

def popupHandler(userid, choice, popupid):
	last_split  = popupid.split('_')
	last_search = int(last_split[2])

	if choice == 8:
		if last_search < 0:
			doCommand(userid, 'shopinfo7')

		elif last_search < 6:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)-7
			doCommand(userid, 'shopinfo%s'%newsearch)

	elif choice == 9:
		if last_search >= len(wcs.wcs.itemdb.getSections()):
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)+7
			doCommand(userid, 'shopinfo%s'%newsearch)

	elif choice < 8:
		#popup = 'shopinfo_%s_%s_7'%(userid, divmod(last_search, 7)[0]*7-(8-choice))
		popup = 'shopinfo_%s_%s_0'%(userid, choice)
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
		item = allvalues[last_search]
		#del allvalues[:last_search - 7]
		#del allvalues[last_search:]

		pname = 'shopinfo_%s_%s_%s'%(userid, choice, last_search)
		popups.append(pname)

		shopinfo = create(pname)

		iteminfo = wcs.wcs.itemdb.getItem(item)
		c = wcs.wcs.shopmenu.canBuy(userid, item)
		text = '->'+str(last_search+1)+'. '+str(iteminfo['name']) if not c else str(last_search+1)+'. '+str(iteminfo['name'])
		shopinfo.addline(text)
		shopinfo.addline('($'+str(iteminfo['cost'])+'|minimum level '+str(iteminfo['level'])+')')
		shopinfo.addline('Buy when you are '+['<death>','<alive>','<death or alive>'][int(iteminfo['dab'])]+' duration '+['<this round>','<untill death>'][int(iteminfo['duration'])])
		shopinfo.addline('Amount in stock: '+str(iteminfo['max']))
		shopinfo.addline('ID: '+item)
		shopinfo.addline(' ')
		info = str(iteminfo['desc']).split('\\n')
		for x in info:
			shopinfo.addline(x)

		shopinfo.menuselect = callBack1

		for x in xrange(1, 7):
			shopinfo.submenu(x, pname)

		if int(iteminfo['cost']) <= getPlayer(userid).cash:
			shopinfo.addline('->7. Buy')
		else:
			shopinfo.addline(' ')

		shopinfo.addline(' ')
		shopinfo.addline('->8. Back')

		if len(allvalues) <= last_search+1:
			shopinfo.addline(' ')
			shopinfo.submenu(9, pname)
		else:
			shopinfo.addline('->9. Next')

		shopinfo.addline('0. Close')

		shopinfo.send(userid)
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

	if choice == 7:
		item = item[last_search]

		c = wcs.wcs.shopmenu.canBuy(userid, item)
		if not 0:
			wcs.wcs.tell(userid, 'shopmenu: purchase', {'item':itemsa[section][item]['name']})
			wcs.wcs.shopmenu.addItem(userid, item, True)

		elif c == 1:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			wcs.wcs.tell(userid, 'shopmenu: too many', {'item':itemsa[section][item]['name']})
		elif c == 2:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			wcs.wcs.tell(userid, 'shopmenu: not enough', {'cash':int(itemsa[section][item]['cost'])-getPlayer(userid).cash,'item':itemsa[section][item]['name']})
		elif c == 3:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			wcs.wcs.tell(userid, 'shopmenu: item restricted', {'item':itemsa[section][item]['name']})
		elif c == 4:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			wcs.wcs.tell(userid, 'shopmenu: section item', {'item':itemsa[section][item]['name'], 'section':section})
		elif c == 5:
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			wcs.wcs.tell(userid, 'shopmenu: can\'t buy', {'item':itemsa[section][item]['name'],'status':['<death>','<alive>','<death or alive>'][int(itemsa[section][item]['dab'])]})

	elif choice == 8:
		if last_search <= 0:
			doCommand(userid)

		elif last_search < 1:
			doCommand(userid, 'shopinfo'+str(last_search))

		else:
			newsearch = int(last_search)-1
			doCommand1(userid, 'shopinfo_%s_%s_%s'%(userid, test, newsearch))

	elif choice == 9:
		if last_search >= len(item):
			send(popupid, userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")

		else:
			newsearch = int(last_search)+1
			doCommand1(userid, 'shopinfo_%s_%s_%s'%(userid, test, newsearch))


callBack = popupHandler
callBack1 = popupHandler1

def getPopups():
	return popups
