import es
from popuplib import create, send, exists
import wcs

popups = []

def doCommand(userid):
	if not exists('wcshelp_main'):
		popups.append('wcshelp_main')
		popup = create('wcshelp_main')
		popup.addline('Chat commands:')
		popup.addline(' wcshelp - This help')
		popup.addline(' changerace - Choose your race')
		popup.addline(' raceinfo - Show info about skills')
		#popup.addline(' shopmenu - buy shop items')
		#popup.addline(' shopinfo - show item info')
		popup.addline(' showxp - Race, level and XP')
		#popup.addline(' showskills - Show all skills levels')
		popup.addline(' resetskills - Reset your skills')
		popup.addline(' spendskills - Spend skill points')
		popup.addline(' playerinfo - Shows info about a player')

		#if wcs.wcs.game == 'dod':
		#	pass
			#popup.addline(' levi - restores levitation level')
			#popup.addline(' showcredits - shows your money')

		popup.addline(' wcsadmin - Admin menu')
		popup.addline(' wcstop - WCS top')
		popup.addline(' wcsrank - WCS rank')
		#popup.addline('____________________')
		#popup.addline(str(wcs.wcs.author))

	send('wcshelp_main', userid)
	es.ServerVar('wcs_ppuser').set(userid)
	es.doblock("wcs/tools/pending/pending")

def getPopups():
	return popups
