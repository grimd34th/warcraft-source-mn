from es import tell, exists
from playerlib import getPlayer
from cmdlib import registerSayCommand, registerClientCommand, unregisterSayCommand, unregisterClientCommand

from wcs import wcs


def load():
	registerSayCommand('ultimate', register, '')
	registerClientCommand('ultimate', register, '')

def unload():
	unregisterSayCommand('ultimate')
	unregisterClientCommand('ultimate')

def register(userid, args):
	if exists('userid', userid):
		player = wcs.getPlayer(userid)
		if int(getPlayer(userid).team) > 1 and not int(getPlayer(userid).isdead):
			returned = wcs.checkEvent1(userid, 'player_ultimate')
			if returned is not None:
				if returned is False:
					tell(userid, '#multi', 'You cannot activate your ultimate now.')
				elif len(returned) == 3 and not returned[0]:
					tell(userid, '#multi', '#lightgreenYou cannot use your ultimate! Cooldown time is #green'+str(returned[1])+' #lightgreenseconds, #green'+str(returned[1]-returned[2])+' left')
