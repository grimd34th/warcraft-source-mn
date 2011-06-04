from playerlib import getPlayer
from usermsg import echo
from gamethread import delayed
from wcs.wcs import strings, tell



thanks = {'Mattie':'For creating EventScripts',
		  'Awuh0':'For creating Es_Tools',
		  'Freddukes':'For the EST-replacement script (and a lot of extra things in the core)',
		  '101Satoon101':'For making his saytextlib (great work!)',
		  'Ojii':'For making his CheapCron',
		  'L\'In20Cible':'For making his PlayerViewLib', 
		  'Craziest':'I used his rank-system (hope you don\'t mind)',
		  'Kryptonite':'For creating the first WCS mod',
		  'Tha Pwned':'The creator of this WCS mod'}

def player_say(ev):
	if ev['text'].lower() in ('wcsthanks','wcsthx'):
		userid = ev['userid']
		tell(userid, 'thanks: console')
		echo(userid, strings('thanks: thank', {}, getPlayer(userid).get('lang')))
		for x in thanks:
			echo(userid, '[WCS Thanks] '+x+': '+thanks[x])

def player_activate(ev):
	if ev['es_steamid'] in ('STEAM_0:0:5712733','STEAM_0:0:8380625','STEAM_0:1:10717798','STEAM_0:1:15131822','STEAM_0:0:5183707','STEAM_0:0:21149716','STEAM_0:1:12649063','STEAM_0:1:5818184'):
		delayed(2, tell, ('#all', 'thanks: thanks to', {'name':ev['es_username']}))
