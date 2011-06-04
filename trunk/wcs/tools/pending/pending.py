import es
import popuplib
from playerlib import getPlayer
import wcs

popups = []


def pending():
	userid = es.ServerVar('wcs_ppuser')
	status = popuplib.active(userid)
	if status['count'] >= 3:
		popuplib.unsendname(str(status['name']), userid)
	if status['count'] >= 7:	
		es.server.queuecmd("kickid %s" % (userid))
		popuplib.close(str(status['name']), userid) 
		