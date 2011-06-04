from es import tell, exists, doblock, ServerVar
from cmdlib import registerClientCommand, unregisterClientCommand, registerSayCommand, unregisterSayCommand
from playerlib import getPlayer
from os.path import isdir

from wcs import wcs


def load():
	registerClientCommand('ability', register, '')
	registerSayCommand('ability', register, '')

def unload():
	unregisterClientCommand('ability')
	unregisterSayCommand('ability')

def register(userid, args):
	if exists('userid', userid):
		player = wcs.getPlayer(userid)
		if int(getPlayer(userid).team) > 1 and not int(getPlayer(userid).isdead):
			value = wcs.wcsgroup.getUser(userid, 'ability')
			if value is None or not value:
				#There's a normal ability (player_ability in skillcfg)
				returned = wcs.checkEvent1(userid, 'player_ability')
				if returned is not None:
					if returned is False:
						tell(userid, '#multi', 'You cannot activate your ability now.')
					elif len(returned) == 3 and not returned[0]:
						tell(userid, '#multi', '#lightgreenYou cannot use your ability! Cooldown time is #green'+str(returned[1])+' #lightgreenseconds, #green'+str(returned[1]-returned[2])+' left')

			else:
				if wcs.gamestarted:
					ServerVar('wcs_userid').set(userid)

					if isdir(wcs.ini.path+'/tools/abilitys/'+str(value)):
						#There's a ordinary ability (player_spawn where it sets the "ability" key to xxx)
						doblock('wcs/tools/abilitys/'+str(value)+'/'+str(value)) #value got to be a valid file and block
				else:
					tell(userid, '#multi', 'You cannot activate your ability now.')
