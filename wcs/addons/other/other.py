import es
from gamethread import delayed
from playerlib import getPlayer
from weaponlib import getWeaponList
from wcs.wcs import wcsgroup, expand, tell
from wcs.core.expand import give

def load():
	es.ServerVar('wcs_space').set(" ")

	wep = []
	for x in getWeaponList('#grenade'):
		wep.append(x)
	es.ServerVar('wcs_wpn_grenades').set('|'.join(wep))

	wep = []
	for x in getWeaponList('#melee'):
		wep.append(x)
	es.ServerVar('wcs_wpn_melee').set('|'.join(wep))

	es.ServerVar('wcs_game_css').set('cstrike')
	es.ServerVar('wcs_game_dods').set('dod')
	es.ServerVar('wcs_game_hl2mp').set('hl2mp')
	es.ServerVar('wcs_game_tf').set('tf')
	es.ServerVar('wcs_game_pvkii').set('pvkii')

def round_end(ev):
	var = int(es.ServerVar('wcs_roundcounter'))
	es.ServerVar('wcs_roundcounter').set(var+1)

def round_end(ev):
	wcsgroup.setUser('T', 'phoenix', 0)
	wcsgroup.setUser('CT', 'phoenix', 0)

def player_death(ev):
	team = int(ev['es_userteam'])
	if team >= 2:
		userid = str(ev['userid'])
		teamv = {2:'T',3:'CT'}[team]
		value = wcsgroup.getUser(teamv, 'phoenix')
		if value:
			wcsgroup.setUser(teamv, 'phoenix', value-1)

			#delayed(2.5, tell, (userid, '#multi', '#lightgreenYou have #greenrespawned #lightgreenbecause of your teammate\'s #greenPhoenix skill.'))
			delayed(2.5, tell, (userid, 'other: phoenix'))
			delayed(3, expand.spawn, userid)

		wcsgroup.setUser(userid, 'ulti_immunity', 0)

'''def player_spawn(ev):
	userid = ev['userid']
	if es.keygetvalue('WCSuserdata', userid, 'reincarnation'):
		wa = es.keygetvalue('WCSuserdata', userid, 'wa')
		wb = es.keygetvalue('WCSuserdata', userid, 'wb')
		p = getPlayer(userid)
		if wa:
			delayed(1, give, (userid, wa))
			delayed(1.5, p.set, ('ammo', ('primary', 50)))
		if wb:
			delayed(1, give, (userid, wb))
			delayed(1.5, p.set, ('ammo', ('secondary', 50)))

		es.keysetvalue('WCSuserdata', userid, 'reincarnation', 0)'''

'''def item_pickup(ev):
	userid = ev['userid']
	if es.keygetvalue('WCSuserdata', userid, 'reincarnation'):
		item = ev['item']
		if item in getWeaponList('#primary'):
			es.keysetvalue('WCSuserdata', userid, 'wa', item)
		if item in getWeaponList('#secondary'):
			es.keysetvalue('WCSuserdata', userid, 'wb')'''
