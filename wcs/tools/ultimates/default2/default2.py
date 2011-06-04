import es
import gamethread
import playerlib
import usermsg
from wcs import wcs



def wcs_ulti_roots():
	userid = int(es.ServerVar('wcs_userid'))
	count = 0

	if es.getplayerteam(userid) >= 2:
		if playerlib.getUseridList('#alive'):
			usermsg.fade(userid, 0, 1, 1, 10, 55, 5, 200)
			x,y,z = es.getplayerlocation(userid)
			radius = float(es.ServerVar('wcs_radius'))
			time = float(es.ServerVar('wcs_freezetime'))

			for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
				x1,y1,z1 = es.getplayerlocation(user)

				if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
					#check for wall between...

					if not wcs.wcsgroup.getUser(user, 'ulti_immunity'):
						playerlib.getPlayer(user).freeze = 1
						gamethread.delayed(time, reset, (user, 'freeze', 0))
						count += 1

					else:
						wcs.tell(user, 'u_ulti_immunity_v')
						wcs.tell(userid, 'u_ulti_immunity_a')

	if count:
		es.centertell(wcs.strings('c_u_entanglingroots', {'count':count}, playerlib.getPlayer(userid).lang))
	else:
		wcs.tell(userid, 'u_roots_failed')
		wcs.cancel(userid, 'player_ultimate')

def wcs_ulti_chain():
	userid = int(es.ServerVar('wcs_userid'))
	count = 0

	if es.getplayerteam(userid) >= 2:
		if playerlib.getUseridList('#alive'):
			usermsg.fade(userid, 0, 2, 1, 240, 240, 240, 100)
			x,y,z = es.getplayerlocation(userid)
			radius = float(es.ServerVar('wcs_radius'))

			for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
				x1,y1,z1 = es.getplayerlocation(user)

				if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
					#check for wall between...

					if not wcs.wcsgroup.getUser(user, 'ulti_immunity'):
						wcs.expand.damage(user, 32, userid)
						count += 1

					else:
						wcs.tell(user, 'u_ulti_immunity_v')
						wcs.tell(userid, 'u_ulti_immunity_a')

	if count:
		es.centertell(wcs.strings('c_u_chainglightning', {'count':count}, playerlib.getPlayer(userid).lang))
	else:
		wcs.tell(userid, 'u_chain_failed')
		wcs.cancel(userid, 'player_ultimate')

def wcs_ulti_suicide():
	userid = int(es.ServerVar('wcs_userid'))

	if es.getplayerteam(userid) >= 2:
		if playerlib.getUseridList('#alive'):
			usermsg.fade(userid, 0, 2, 1, 240, 240, 240, 100)
			x,y,z = es.getplayerlocation(userid)
			radius = float(es.ServerVar('wcs_radius'))
			magnitude = float(es.ServerVar('wcs_magnitude'))
			v = round(radius * magnitude) / 150

			for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
				x1,y1,z1 = es.getplayerlocation(user)

				if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
					#check for wall between...

					if not wcs.wcsgroup.getUser(user, 'ulti_immunity'):
						if wcs.friendlyexplosion:
							wcs.effect.effect.Explosion(es.getplayerlocation(user), IMagniTude=magnitude, IRadiusOverride=radius, HOwner=es.getplayerhandle(userid))
						else:
							wcs.expand.damage(user, v, userid)

					else:
						wcs.tell(user, 'u_ulti_immunity_v')
						wcs.tell(userid, 'u_ulti_immunity_a')




def reset(userid, what, default):
	if es.exists('userid', userid):
		setattr(playerlib.getPlayer(userid), what, default)
