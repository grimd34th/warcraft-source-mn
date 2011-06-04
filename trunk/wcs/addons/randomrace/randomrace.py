from wcs.wcs import logging, getPlayer, racedb
from random import choice

races = racedb.getAll().keys()


def player_death(ev):
	if ev['es_steamid'] == 'BOT':
		race = choice(races)
		getPlayer(ev['userid']).changeRace(race, False)

		logging.log('randomrace: Information: Setting bot\'s race to: '+race, 2)
