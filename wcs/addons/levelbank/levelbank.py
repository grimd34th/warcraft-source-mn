from es import tell, exists, getplayername, getplayersteamid
from cmdlib import registerSayCommand, registerClientCommand, unregisterSayCommand, unregisterClientCommand
from popuplib import create, easymenu, find
from playerlib import uniqueid, getPlayerList
from wcs.wcs import getPlayer, admin, dataAPI



db = dataAPI.DB('levelbank')


def load():
	registerClientCommand('wcsbankadmin', register, '')
	registerSayCommand('wcsbankadmin', register, '')
	registerClientCommand('spendslevels', spendslevelsCmd, '')
	registerSayCommand('spendslevels', spendslevelsCmd, '')

	popup = create('wcsbanklevel')
	popup.addline('Spend your levels here')
	popup.addline(' ')
	popup.addline(' ')
	popup.addline('->1. 1')
	popup.addline('->2. 5')
	popup.addline('->3. 10')
	popup.addline('->4. 25')
	popup.addline('->5. 100')
	popup.addline('->6. 250')
	popup.addline('->7. 1000')
	popup.addline('->8. 2500')
	popup.addline(' ')
	popup.addline('0. Close')

	popup.menuselect = menuselect

	popup.submenu(9, 'wcsbanklevel')

	db.load()

def unload():
	unregisterClientCommand('wcsbankadmin')
	unregisterSayCommand('wcsbankadmin')
	unregisterClientCommand('spendslevels')
	unregisterSayCommand('spendslevels')

	db.save()

def es_map_start(ev):
	db.save()

def register(userid, args):
	if admin.getPlayer(userid).hasFlag('wcsbankadmin'):
		menu(userid)
	else:
		tell(userid, '#multi', '#lightgreenYou\'re #greennot #lightgreenan WCS-bank admin')

def spendslevelsCmd(userid, args):
	steamid = getplayersteamid(userid)

	if steamid in db and db[steamid]:
		send(userid)
	else:
		tell(userid, 'You got 0 levels in the bank.')

def menu(userid):
	popupname = 'wcsbank_'+str(userid)
	popup = easymenu(popupname, '_popup_choice', menuHandler)
	popup.settitle('Select a player')

	popup.c_beginsep = None
	popup.c_pagesep = None

	for user in getPlayerList('#human'):
		popup.addoption(user.userid, user.name)

	popup.send(userid)

def menuHandler(userid, target, popupid):
	if exists('userid', target):
		popup = create('wcsbankselect_'+str(target))
		popup.addline('How many levels will you give '+str(getplayername(target)))
		popup.addline('->1. 1')
		popup.addline('->2. 5')
		popup.addline('->3. 10')
		popup.addline('->4. 25')
		popup.addline('->5. 100')
		popup.addline('->6. 250')
		popup.addline('->7. 1000')
		popup.addline('->8. 2500')
		popup.addline('->9. Back')
		popup.addline('0. Close')

		popup.menuselect = menuHandlerGetsHandled

		popup.send(userid)
	else:
		tell(userid, 'Unknown player')
		menu(userid)

def menuHandlerGetsHandled(userid, choice, popupid):
	if choice < 9:
		target = popupid.split('_')[1]
		if exists('userid', target):
			levels = [1,5,10,25,100,250,1000,2500][choice-1]
			steamid = getplayersteamid(target)
			if not steamid in db:
				db[steamid] = 0

			db[steamid] += levels
			tell(userid, 'You gave '+str(levels)+' bank-levels to '+str(getplayername(target)))
			tell(target, 'You gained '+str(levels)+' bank-levels from an admin')
		else:
			tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 9:
		menu(userid)

def menuselect(userid, choice, popupid):
	if choice < 9:
		steamid = getplayersteamid(userid)
		if steamid in db:
			paid   = [1,5,10,25,100,250,1000,2500][choice-1]
			if paid <= db[steamid]:
				getPlayer(userid).race.addLevel(paid)
				db[steamid] -= paid
				tell(userid, 'You got '+str(db[steamid])+' levels left in the bank.')
				if not db[steamid]:
					del db[steamid]
			else:
				tell(userid, 'Not enough bank-levels!')
				send(userid)

		else:
			tell(userid, 'Not enough bank-levels!')
			send(userid)

def send(userid):
	steamid = getplayersteamid(userid)
	if steamid in db:
		value = db[value]
	else:
		value = 0

	popup = find('wcsbanklevel')
	popup.modline(2, 'You got currently '+str(value)+' levels')
	popup.send(userid)
