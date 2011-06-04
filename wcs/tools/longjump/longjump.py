from es import getplayerprop, setplayerprop, exists
from wcs.wcs import wcsgroup, expand

def player_jump(ev):
	userid = str(ev['userid'])
	if exists('userid', userid):
		value = wcsgroup.getUser(userid, 'longjump')
		if value is not None:
			value = float(value)

		if value:
			if value < 1:
				value = 1.0

			tmp = float(getplayerprop(userid, 'CBasePlayer.localdata.m_vecVelocity[0]')) * value
			tmp1 = float(getplayerprop(userid, 'CBasePlayer.localdata.m_vecVelocity[1]')) * value
			setplayerprop(userid, 'CBasePlayer.localdata.m_vecBaseVelocity', ','.join([str(tmp), str(tmp1), '0']))
			#expand.push(userid, (tmp, tmp1, 0))
