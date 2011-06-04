from es import exists, ServerVar, getplayername, getplayersteamid, escinputbox, getuserid, server, msg, addons
from cmdlib import registerSayCommand, registerClientCommand, unregisterSayCommand, unregisterClientCommand
from playerlib import getPlayer as pplayer
from popuplib import easymenu, create
from playerlib import getPlayer, getPlayerList

from wcs import wcs

convert = lambda x: int(not x)
reloadFunc = True

def load():
	registerSayCommand('wcsadmin', register, '')
	registerClientCommand('wcsadmin', register, '')

	registerClientCommand('wcsgivexp', giveXpCmd, '')
	registerClientCommand('wcsgivelevel', giveLevelCmd, '')
	registerClientCommand('wcsgivecash', giveCashCmd, '')

	addons.registerSayFilter(sayFilter)

def unload():
	unregisterSayCommand('wcsadmin')
	unregisterClientCommand('wcsadmin')

	unregisterClientCommand('wcsgivexp')
	unregisterClientCommand('wcsgivelevel')
	unregisterClientCommand('wcsgivecash')

	addons.unregisterSayFilter(sayFilter)

def sayFilter(userid, text, teamonly):
	if text.strip('"').startswith('&') and wcs.admin.getPlayer(userid).hasFlag('wcsadmin'):
		text = text.strip('"')[1:].strip()
		#msg('#multi', '\x05WcsAdmin #lightgreen'+getplayername(userid)+'\x05: #lightgreen'+text)
		msg('#lightgreen', '[WcsAdmin] '+getplayername(userid)+': '+text)
		return (0,0,False)

	return (userid, text, teamonly)


def register(userid, args):
	player = wcs.admin.getPlayer(userid)
	if player.hasFlag('wcsadmin'):
		for x in ('wcsadmin_addadmins',
				'wcsadmin_removeadmins',
				'wcsadmin_editadmins',
				'wcsadmin_settings',
				'wcsadmin_givexp',
				'wcsadmin_givelevels',
				'wcsadmin_givecash',
				'wcsadmin_resetrace',
				'wcsadmin_resetplayer'):
			if not x in player:
				player.setFlag(x, 0)

		menu(userid)
	else:
		wcs.tell(userid, 'wcsadmin: not admin')

def menu(userid):
	popupname = 'wcsadmin_'+str(userid)
	popup = easymenu(popupname, '_popup_choice', menuHandler)
	popup.settitle('Select a player')

	popup.c_beginsep = None
	popup.c_pagesep = None

	number = 0
	playerlist = getPlayerList('#all')
	for user in playerlist:
		number += 1
		if number == 7:
			popup.addoption('setting', '< WCS settings >')
			popup.addoption(user.userid, user.name+' (level '+str(wcs.getPlayer(user.userid).player.totallevel)+')')
			number = 1
		else:
			popup.addoption(user.userid, user.name+' (level '+str(wcs.getPlayer(user.userid).player.totallevel)+')')

	while number < 7:
		number += 1
		if number == 7:
			if wcs.admin.getPlayer(userid).hasFlag('wcsadmin_settings'):
				popup.addoption('setting', '< WCS settings >')
			else:
				popup.addoption('x', ' ', state=0)
		else:
			popup.addoption('x', ' ', state=0)

	popup.send(userid)

def menuHandler(userid, choice, popupid):
	if str(choice).isdigit():
		if exists('userid', choice):
			menuPlayer(userid, choice)
		else:
			wcs.tell(userid, 'wcsadmin: unknown player')
			#tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 'setting':
		menuSetting(userid)

def menuPlayer(userid, target):
	player = wcs.admin.getPlayer(userid)
	player1 = wcs.admin.getPlayer(target)
	popupname = 'wcsadmin_'+str(userid)+'_'+str(target)
	popup = create(popupname)

	popup.menuselect = menuPlayerHandler

	popup.addline('  '+getplayername(target))
	popup.addline(' ')
	popup.addline('Please make a selection:')

	if player.hasFlag('wcsadmin_givexp'):
		popup.addline('->1. Give XP')
	else:
		popup.addline(' ')
		popup.submenu(1, popupname)

	if player.hasFlag('wcsadmin_givelevels'):
		popup.addline('->2. Give levels')
	else:
		popup.addline(' ')
		popup.submenu(2, popupname)

	if player.hasFlag('wcsadmin_givecash'):
		popup.addline('->3. Give cash')
	else:
		popup.addline(' ')
		popup.submenu(3, popupname)

	if player.hasFlag('wcsadmin_addadmins') and not player1.hasFlag('wcsadmin') and not getplayersteamid(target) == 'BOT':
		popup.addline('->4. Add as an WcsAdmin')
	elif player.hasFlag('wcsadmin_removeadmins') and player1.hasFlag('wcsadmin') and not getplayersteamid(target) == 'BOT':
		popup.addline('->4. Remove their WcsAdmin')
	else:
		popup.addline(' ')
		popup.submenu(4, popupname)

	if player1.hasFlag('wcsadmin') and player.hasFlag('wcsadmin_editadmins') and not getplayersteamid(target) == 'BOT':
		popup.addline('->5. Edit settings')
	else:
		popup.addline(' ')
		popup.submenu(5, popupname)

	if player.hasFlag('wcsadmin_resetrace'):
		popup.addline('->6. Reset player (current race)')
	else:
		popup.addline(' ')
		popup.submenu(6, popupname)

	if player.hasFlag('wcsadmin_resetplayer'):
		popup.addline('->7. Reset player (all)')
	else:
		popup.addline(' ')
		popup.submenu(7, popupname)

	popup.addline('->8. Back')
	popup.addline(' ')
	popup.addline('->0. Close')

	popup.submenu(9, popupname)

	popup.send(userid)


def menuPlayerHandler(userid, choice, popupid):
	target = str(popupid.split('_')[2])
	player = wcs.admin.getPlayer(userid)
	player1 = wcs.admin.getPlayer(target)

	if choice in (1, 2, 3):
		if exists('userid', target):
			if {1:player.hasFlag('wcsadmin_givexp'), 2:player.hasFlag('wcsadmin_givelevels'), 3:player.hasFlag('wcsadmin_givecash')}[choice]:
				amountMenu('wcsadmin_'+target+'_0', {1:giveXp, 2:giveLevel, 3:giveCash}[choice]).send(userid)
		else:
			wcs.tell(userid, 'wcsadmin: unknown player')
			#tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 4:
		if player.hasFlag('wcsadmin_addadmins') and not player1.hasFlag('wcsadmin') and not getplayersteamid(target) == 'BOT':
			player1.setFlag('wcsadmin')
			for x in ('wcsadmin_addadmins',
					'wcsadmin_editadmins',
					'wcsadmin_settings',
					'wcsadmin_givexp',
					'wcsadmin_givelevels',
					'wcsadmin_givecash',
					'wcsadmin_resetrace',
					'wcsadmin_resetplayer'):
				if not x in player1:
					player1.setFlag(x, 0)

			wcs.tell(target, 'wcsadmin: got admin')
			wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') added '+getplayername(target)+' ('+getplayersteamid(target)+') as an WcsAdmin')

		elif player.hasFlag('wcsadmin_removeadmins') and player1.hasFlag('wcsadmin') and not getplayersteamid(target) == 'BOT':
			player1.setFlag('wcsadmin', 0)
			wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') removed '+getplayername(target)+' ('+getplayersteamid(target)+') as an WcsAdmin')

	elif choice == 5:
		if player1.hasFlag('wcsadmin') and player.hasFlag('wcsadmin_editadmins') and not getplayersteamid(target) == 'BOT':
			menuEditer(userid, target)

	elif choice in (6, 7):
		if exists('userid', target):
			if choice == 6:
				if player.hasFlag('wcsadmin_resetrace'):
					menuDeletePlayer1(userid, target)
			else:
				if player.hasFlag('wcsadmin_resetplayer'):
					menuDeletePlayer2(userid, target)
		else:
			wcs.tell(userid, 'wcsadmin: unknown player')
			#tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 8:
		menu(userid)

def menuDeletePlayer1(userid, target):
	popup = create('wcsadmin_confirm_'+str(target))

	popup.menuselect = menuDeletePlayerHandler1

	popup.addline('You\'re about to reset '+str(getplayername(target))+'\'s')
	popup.addline('race permanently.')
	popup.addline(' ')
	popup.addline('Will you proceed?')
	popup.addline('This cannot be recovered!')
	popup.addline('->1. Yes')
	popup.addline('->2. No')
	popup.addline(' ')
	popup.addline('->8. Back')
	popup.addline(' ')
	popup.addline('0. Close')

	for x in (3,4,5,6,7,9):
		popup.submenu(x, 'wcsadmin_confirm_'+str(target))

	popup.send(userid)

def menuDeletePlayerHandler1(userid, choice, popupid):
	target = popupid.split('_')[2]
	if choice == 1:
		player = wcs.getPlayer(target)

		player.delRace()

		wcs.tell(target, 'wcsadmin: reseted race')
		#tell(target, 'You got resetted!')
		wcs.tell(userid, 'wcsadmin: resetter race', {'name':getplayername(target)})
		#tell(userid, 'You resetted '+str(getplayername(target))+'\'s race.')

	elif choice == 2:
		menuPlayer(userid, target)

	elif choice == 8:
		menuPlayer(userid, target)

def menuDeletePlayer2(userid, target):
	popup = create('wcsadmin_confirm_'+str(target))

	popup.menuselect = menuDeletePlayerHandler2

	popup.addline('WCSadmin')
	popup.addline(' ')
	popup.addline('You\'re about to')
	popup.addline('completely reset '+str(getplayername(target)))
	popup.addline('permanently.')
	popup.addline(' ')
	popup.addline('Will you proceed?')
	popup.addline('This cannot be recovered!')
	popup.addline('->1. Yes')
	popup.addline('->2. No')
	popup.addline(' ')
	popup.addline('->8. Back')
	popup.addline(' ')
	popup.addline('0. Close')

	for x in (3,4,5,6,7,9):
		popup.submenu(x, 'wcsadmin_confirm_'+str(target))

	popup.send(userid)

def menuDeletePlayerHandler2(userid, choice, popupid):
	target = popupid.split('_')[2]
	if choice == 1:
		player = wcs.getPlayer(target)

		player.delPlayer()

		wcs.tell(target, 'wcsadmin: reseted all')
		#tell(target, 'You got completely resetted!')
		wcs.tell(userid, 'wcsadmin: resetter all', {'name':getplayername(target)})
		#tell(userid, 'You resetted '+str(getplayername(target))+' completely.')

	elif choice == 2:
		menuPlayer(userid, target)

	elif choice == 8:
		menuPlayer(userid, target)

def menuEditer(userid, target):
	pname = 'wcsadmin_edit_'+str(userid)+'_'+str(target)
	popup = create(pname)

	popup.menuselect = menuEditerHandler

	popup.addline('  '+getplayername(target))
	popup.addline(' ')
	popup.addline('Please make a selection:')

	player = wcs.admin.getPlayer(target).hasFlag

	popup.addline('->1. Give XP ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_givexp'))]+']')
	popup.addline('->2. Give levels ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_givelevels'))]+']')
	popup.addline('->3. Give cash ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_givecash'))]+']')
	popup.addline('->4. Add an WcsAdmin ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_addadmins'))]+']')
	popup.addline('->5. Remove an WcsAdmin ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_removeadmins'))]+']')
	popup.addline('->6. Edit WcsAdmin settings ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_editadmins'))]+']')
	popup.addline('->7. Reset player (current race) ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_resetrace'))]+']')

	popup.addline('->8. Back')
	popup.addline('->9. Next')
	popup.addline('0. Close')

	popup.send(userid)

def menuEditer1(userid, target):
	pname = 'wcsadmin_edit_'+str(userid)+'_'+str(target)
	popup = create(pname)

	popup.menuselect = menuEditerHandler1

	popup.addline('  '+getplayername(target))
	popup.addline(' ')
	popup.addline('Please make a selection:')

	player = wcs.admin.getPlayer(target).hasFlag

	popup.addline('->1. Reset player (all) ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_resetplayer'))]+']')
	popup.addline('->2. WCS settings ['+{1:'ON',0:'OFF'}[convert(player('wcsadmin_settings'))]+']')
	for x in xrange(3, 8):
		popup.addline(' ')
		popup.submenu(x, pname)

	popup.submenu(9, pname)

	popup.addline('->8. Back')
	popup.addline(' ')
	popup.addline('0. Close')

	popup.send(userid)

def menuEditerHandler(userid, choice, popupid):
	target = popupid.split('_')[3]

	player = wcs.admin.getPlayer(target)

	if choice == 1:
		nv = convert(player.hasFlag('wcsadmin_givexp'))
		player.setFlag('wcsadmin_givexp', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_givexp" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)
	elif choice == 2:
		nv = convert(player.hasFlag('wcsadmin_givelevels'))
		player.setFlag('wcsadmin_givelevels', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_givelevels" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)
	elif choice == 3:
		nv = convert(player.hasFlag('wcsadmin_givecash'))
		player.setFlag('wcsadmin_givecash', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_givecash" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)
	elif choice == 4:
		nv = convert(player.hasFlag('wcsadmin_addadmins'))
		player.setFlag('wcsadmin_addadmins', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_addadmins" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)
	elif choice == 5:
		nv = convert(player.hasFlag('wcsadmin_removeadmins'))
		player.setFlag('wcsadmin_removeadmins', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_removeadmins" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)
	elif choice == 6:
		nv = convert(player.hasFlag('wcsadmin_editadmins'))
		player.setFlag('wcsadmin_editadmins', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_editadmins" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)
	elif choice == 7:
		nv = convert(player.hasFlag('wcsadmin_resetrace'))
		player.setFlag('wcsadmin_resetrace', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_resetrace" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer(userid, target)

	elif choice == 8:
		menuPlayer(userid, target)
	elif choice == 9:
		menuEditer1(userid, target)

def menuEditerHandler1(userid, choice, popupid):
	target = popupid.split('_')[3]

	player = wcs.admin.getPlayer(target)

	if choice == 1:
		nv = convert(player.hasFlag('wcsadmin_resetplayer'))
		player.setFlag('wcsadmin_resetplayer', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_resetplayer" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer1(userid, target)
	elif choice == 2:
		nv = convert(player.hasFlag('wcsadmin_settings'))
		player.setFlag('wcsadmin_settings', nv)
		wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') changed flag "wcsadmin_settings" on player '+getplayername(target)+' ('+getplayersteamid(target)+') to '+str(nv))
		menuEditer1(userid, target)

	elif choice == 8:
		menuEditer(userid, target)

def menuSetting(userid):
	popupname = 'wcsadmin_setting_'+str(userid)
	popup = create(popupname)
	popup.menuselect = menuSettingHandler

	popup.addline('WCS settings:')
	popup.addline(' ')
	popup.addline('->1. Give all XP')
	popup.addline('->2. Give all levels')
	popup.addline('->3. Give all cash')
	popup.addline('->4. Toogle friendlyfire (current: '+{1:'On',0:'Off'}[bool(int(ServerVar('mp_friendlyfire')))]+')')
	if reloadFunc:
		popup.addline('->5. Reload mod (and mapchange)')
	else:
		popup.addline(' ')
		popup.submenu(5, popupname)
	popup.addline('->6. Save admins')
	popup.addline(' ')
	popup.addline('->8. Back')
	popup.addline(' ')
	popup.addline('0. Close')

	popup.submenu(6, popupname)
	popup.submenu(7, popupname)
	popup.submenu(9, popupname)

	popup.send(userid)

def menuSettingHandler(userid, choice, popupid):
	if choice in (1, 2, 3):
		amountMenu('wcsadmin_all_0', {1:giveXp, 2:giveLevel, 3:giveCash}[choice]).send(userid)

	elif choice == 4:
		if int(ServerVar('mp_friendlyfire')):
			ServerVar('mp_friendlyfire').set(0)
			wcs.tell(userid, 'wcsadmin: friendlyfire off')
			#tell(userid, 'You turned mp_friendlyfire off.')
			menuSetting(userid)
		else:
			ServerVar('mp_friendlyfire').set(1)
			wcs.tell(userid, 'wcsadmin: friendlyfire on')
			#tell(userid, 'You turned mp_friendlyfire on.')
			menuSetting(userid)

	elif choice == 5:
		if reloadFunc:
			server.queuecmd('es_xmsg RELOADING WCS!;es_xdelayed .1 es_xunload wcs;es_xdelayed 2 es_xload wcs;es_xdelayed 3 es_xmsg CHANGEING MAP!;es_xdelayed 5 changelevel '+wcs.curmap)

	elif choice == 6:
		wcs.admin.admins.save()
		wcs.tell(userid, 'wcsadmin: saved file')

	elif choice == 8:
		menu(userid)


def amountMenu(name, function):
	popup = create(name)

	popup.menuselect = function

	popup.addline('WCSadmin')

	popup.addline('->1. 1')
	popup.addline('->2. 10')
	popup.addline('->3. 100')
	popup.addline('->4. 500')
	popup.addline('->5. Custom')
	popup.addline(' ')
	popup.addline(' ')
	popup.addline('->8. Back')
	popup.addline(' ')
	popup.addline('0. Close')

	popup.submenu(6, name)
	popup.submenu(7, name)
	popup.submenu(9, name)

	return popup

valueamount = {1:1,
			   2:10,
			   3:100,
			   4:500}

def giveXp(userid, choice, popupid):
	popup = popupid.split('_')
	target = popup[1]

	if choice < 6 or int(popup[2]):
		if target.isdigit():
			if not exists('userid', target):
				target = str(getuserid(target))

		if (exists('userid', target) and not target == 'all') or target == 'all':
			if choice == 5 and not int(popup[2]):
				escinputbox(30, userid, 'WCSadmin - Give XP', 'Enter the amount' , 'wcsgivexp '+target)

			elif choice in xrange(1,5) and not int(popup[2]):
				if target == 'all':
					for user in getPlayerList('#all'):
						wcs.getPlayer(user).giveXp(valueamount[choice])
						wcs.tell(user, 'wcsadmin: all gained xp', {'admin':getplayername(userid),'xp':valueamount[choice]})
						#tell(user, 'All have gained '+str(valueamount[choice])+' XP.')
				else:
					wcs.getPlayer(target).giveXp(valueamount[choice])
					wcs.tell(target, 'wcsadmin: you gained xp', {'admin':getplayername(userid),'target':getplayername(target),'xp':valueamount[choice]})
					#tell(target, 'You have gained '+str(valueamount[choice])+' XP.')

			else:
				if target == 'all':
					for user in getPlayerList('#all'):
						wcs.getPlayer(user).giveXp(choice)
						wcs.tell(user, 'wcsadmin: all gained xp', {'admin':getplayername(userid),'xp':choice})
						#tell(user, 'All have gained '+str(choice)+' XP.')
				else:
					wcs.getPlayer(target).giveXp(choice)
					wcs.tell(target, 'wcsadmin: you gained xp', {'admin':getplayername(userid),'target':getplayername(target),'xp':choice})
					#tell(target, 'You have gained '+str(choice)+' XP.')
		else:
			wcs.tell(userid, 'wcsadmin: unknown player', {})
			#tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 8:
		if target == 'all':
			menuSetting(userid)
		else:
			menuPlayer(userid, target)

def giveLevel(userid, choice, popupid):
	popup = popupid.split('_')
	target = popup[1]

	if choice < 6 or int(popup[2]):
		if target.isdigit():
			if not exists('userid', target):
				target = str(getuserid(target))

		if (exists('userid', target) and not target == 'all') or target == 'all':
			if choice == 5 and not int(popup[2]):
				escinputbox(30, userid, 'WCSadmin - Give Levels', 'Enter the amount' , 'wcsgivelevel '+target)

			elif choice in xrange(1,5) and not int(popup[2]):
				if target == 'all':
					for user in getPlayerList('#all'):
						wcs.getPlayer(user).giveLevel(valueamount[choice])
						wcs.tell(user, 'wcsadmin: all gained level', {'admin':getplayername(userid),'level':valueamount[choice]})
						#tell(user, 'All have gained '+str(valueamount[choice])+' level.')
				else:
					wcs.getPlayer(target).giveLevel(valueamount[choice])
					wcs.tell(target, 'wcsadmin: you gained level', {'admin':getplayername(userid),'target':getplayername(target),'level':valueamount[choice]})
					#tell(target, 'You have gained '+str(valueamount[choice])+' level.')

			else:
				if target == 'all':
					for user in getPlayerList('#all'):
						wcs.getPlayer(user).giveLevel(choice)
						wcs.tell(user, 'wcsadmin: all gained level', {'admin':getplayername(userid),'level':choice})
						#tell(user, 'All have gained '+str(choice)+' level.')
				else:
					wcs.getPlayer(target).giveLevel(choice)
					wcs.tell(target, 'wcsadmin: you gained level', {'admin':getplayername(userid),'target':getplayername(target),'level':choice})
					#tell(target, 'You have gained '+str(choice)+' level.')
		else:
			wcs.tell(userid, 'wcsadmin: unknown player')
			#tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 8:
		if target == 'all':
			menuSetting(userid)
		else:
			menuPlayer(userid, target)

def giveCash(userid, choice, popupid):
	popup = popupid.split('_')
	target = popup[1]

	if choice < 6 or int(popup[2]):
		if target.isdigit():
			if not exists('userid', target):
				target = str(getuserid(target))

		if (exists('userid', target) and not target == 'all') or target == 'all':
			if choice == 5 and not int(popup[2]):
				escinputbox(30, userid, 'WCSadmin - Give Cash', 'Enter the amount' , 'wcsgivecash '+target)

			elif choice in xrange(1,5) and not int(popup[2]):
				if target == 'all':
					for user in getPlayerList('#all'):
						pplayer(user).cash += valueamount[choice]
						wcs.tell(user, 'wcsadmin: all gained cash', {'admin':getplayername(userid),'cash':valueamount[choice]})
						#tell(user, 'All have gained $'+str(valueamount[choice])+'.')
				else:
					pplayer(target).cash += valueamount[choice]
					wcs.tell(target, 'wcsadmin: you gained cash', {'admin':getplayername(userid),'target':getplayername(target),'cash':valueamount[choice]})
					#tell(target, 'You have gained $'+str(valueamount[choice])+'.')

			else:
				if target == 'all':
					for user in getPlayerList('#all'):
						pplayer(user).cash += choice
						wcs.tell(user, 'wcsadmin: all gained cash', {'admin':getplayername(userid),'cash':choice})
						#tell(user, 'All have gained $'+str(choice)+'.')
				else:
					pplayer(target).cash += choice
					wcs.tell(target, 'wcsadmin: you gained cash', {'admin':getplayername(userid),'target':getplayername(target),'cash':choice})
					#tell(target, 'You have gained $'+str(choice)+'.')
		else:
			wcs.tell(userid, 'wcsadmin: unknown player')
			#tell(userid, 'Unknown player')
			menu(userid)

	elif choice == 8:
		if target == 'all':
			menuSetting(userid)
		else:
			menuPlayer(userid, target)



def giveXpCmd(userid, args):
	if len(args) == 2:
		player = wcs.admin.getPlayer(userid)
		target, amount = args
		amount = str(amount)

		if player.hasFlag('wcsadmin') and player.hasFlag('wcsadmin_givexp'):
			if amount.isdigit() and int(amount):
				giveXp(userid, int(amount), 'wcsadmin_'+str(target)+'_1')
			else:
				wcs.tell(userid, 'wcsadmin: unknown amount')
				#tell(userid, 'Unknown amount')
				escinputbox(30, userid, 'WCSadmin - Give XP', 'Enter the amount' , 'wcsgivexp '+str(target))
		else:
			wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') tried to give '+str(amount)+' xp to '+getplayername(target)+' ('+getplayersteamid(target)+') but failed')

def giveLevelCmd(userid, args):
	if len(args) == 2:
		player = wcs.admin.getPlayer(userid)
		target, amount = args
		amount = str(amount)

		if player.hasFlag('wcsadmin') and player.hasFlag('wcsadmin_givelevels'):
			if amount.isdigit() and int(amount):
				giveLevel(userid, int(amount), 'wcsadmin_'+str(target)+'_1')
			else:
				wcs.tell(userid, 'wcsadmin: unknown amount')
				#tell(userid, 'Unknown amount')
				escinputbox(30, userid, 'WCSadmin - Give Level', 'Enter the amount' , 'wcsgivelevel '+str(target))
		else:
			wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') tried to give '+str(amount)+' levels to '+getplayername(target)+' ('+getplayersteamid(target)+') but failed')

def giveCashCmd(userid, args):
	if len(args) == 2:
		player = wcs.admin.getPlayer(userid)
		target, amount = args
		amount = str(amount)

		if player.hasFlag('wcsadmin') and player.hasFlag('wcsadmin_givecash'):
			if amount.isdigit() and int(amount):
				giveCash(userid, int(amount), 'wcsadmin_'+str(target)+'_1')
			else:
				wcs.tell(userid, 'wcsadmin: unknown amount')
				#tell(userid, 'Unknown amount')
				escinputbox(30, userid, 'WCSadmin - Give Cash', 'Enter the amount' , 'wcsgivecash '+str(target))
		else:
			wcs.logging.log('wcsadmin: Information: '+getplayername(userid)+' ('+getplayersteamid(userid)+') tried to give '+str(amount)+' cash to '+getplayername(target)+' ('+getplayersteamid(target)+') but failed')
