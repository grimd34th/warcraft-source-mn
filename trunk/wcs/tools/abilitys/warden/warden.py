import es
from wcs import wcs

try:
	es.load('wcs/addons/cmdskillspy')

	cmdskillspy = es.import_addon('wcs/addons/cmdskillspy')
except ImportError:
	cmdskillspy = None

def warden():
	userid = str(es.ServerVar('wcs_userid'))
	count = int(wcs.wcsgroup.getUser(userid, 'ability_count'))

	if count:
		param = wcs.wcsgroup.getUser(userid, 'ability_parameter')

		if param:
			param = param.split('_')
			team = int(es.getplayerteam(userid))

			if team == 2:
				teamtarget = '3'
				teamtargetn = '#ct'
				color = '255 0 10 150'

			elif team == 3:
				teamtarget = '2'
				teamtargetn = '#t'
				color = '10 0 255 150'

			x,y,z = es.getplayerlocation(userid)

			if es.ServerVar('wcs_cfg_graphicfx'):
				if wcs.effect.effect.EST:
					wcs.effect.effect.est_effect(11, '#a', 0, 'sprites/purpleglow1.vmt', x, y, z+120, param[0], 2, 50)
					wcs.effect.effect.est_effect(3, '#a', 0, 'sprites/lgtning.vmt', x, y, z+120, x, y, z, param[0], 20, 20, color)

				else:
					wcs.effect.effect.BlueCircle((x,y,z+120), BaseSpread=30, RenderColor=color.split(' '), Delayed=float(param[0]))

			if cmdskillspy:
				cmdskillspy.warden([userid, param[0], param[1], param[2], teamtarget, teamtargetn, x, y, z, str(es.ServerVar('wcs_wardencounter'))])
			else:
				es.server.queuecmd('wcs_warden '+userid+' '+param[0]+' '+param[1]+' '+param[2]+' '+teamtarget+' '+teamtargetn+' '+str(x)+' '+str(y)+' '+str(z)+' '+str(es.ServerVar('wcs_wardencounter')))

			wcs.tell(userid, 'a_wardencreated')

		if count and not count == -1:
			wcs.wcsgroup.setUser(userid, 'ability_count', count-1)

	else:
		wcs.tell(userid, 'a_failed')