import es
import gamethread
from vecmath import Vector
from wcs.wcs import effect
from wcs.core.expand import give

effect = effect.effect


dice = es.ServerVar('wcs_dice')
chance = es.ServerVar('wcs_chance')
suserid = es.ServerVar('wcs_userid')
splayer = es.ServerVar('wcs_player')
ev = es.event_var

def load():
	es.ServerVar('wcs_WCSeffectsVersion', 'Beta 0.1').makepublic()
	es.ServerVar('wcs_WCSeffects', 'coded by www.Wcs-Lagerhaus.de').makepublic()

def undead():
	if dice <= 60:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			v[2] += 20
			q[2] += 20
			effect.est_Effect(3, '#a', 0, 'sprites/shellchrome.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 10, 10, 255, 0, 0, es.ServerVar('wcs_alpha'))
			effect.est_Effect(3, '#a', 0, 'sprites/tp_beam001.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 10, 10, 255, 0, 0, es.ServerVar('wcs_alpha'))
			effect.est_Effect(3, '#a', 0, 'sprites/lgtning.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 2, 2, 255, 255, 255, es.ServerVar('wcs_alpha'))
			effect.est_Effect(10, '#a', 0, 'sprites/shellchrome.vmt', q[0], q[1], q[2]+25, 1, 10, 0.5, 40, 500, 255, 255, 0, 0, 100, 255)

def hualianz():
	if dice <= 60:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'sprites/cbbl_smoke.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 10, 10, 255, 255, 255, es.ServerVar('wcs_alpha'))
			effect.est_Effect(10, '#a', 0, 'sprites/cbbl_smoke.vmt', q[0], q[1], q[2]+25, 1, 10, 0.5, 40, 500, 255, 255, 255, 255, 100, 255)

def humanspawn():
	if effect.EST:
		q = Vector(es.getplayerlocation(str(splayer)))
		effect.est_Effect(3, '#a', 0, 'sun/overlay.vmt', 0, 0, 900, v[0], v[1], v[2], 2, 20, 11, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.1, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.2, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 0, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.3, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.4, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.5, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.6, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.7, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.8, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 0.9, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 1.8, 255, 255, 255, 255, 1)
		effect.est_Effect(10, '#a', 10, 'sun/overlay.vmt', 0, 0, 900, 10, 5000, 2, 100, 300, 0.8, 255, 255, 255, 255, 1)

def orc():
	if dice <= 15:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'sprites/plasma.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 10, 10, 0, 255, 0, es.ServerVar('wcs_alpha'))
			effect.est_Effect(3, '#a', 0, 'sprites/heatwave.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 1, 1, 0, 255, 0, es.ServerVar('wcs_alpha'))

def orcspawn():
	userid = ev['userid']
	give(userid, 'point_tesla')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'm_Color 255 71 36')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'm_flRadius 600')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'beamcount_min 1000')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'beamcount_max 6000')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'thick_min 10')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'thick_max 6')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'lifetime_min .1')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'lifetime_max .4')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'interval_min .1')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'interval_max .2')
	es.fire(userid, 'point_tesla', 'AddOutPut', 'texture sprites/lgtning.vmt')
	es.fire(userid, 'point_tesla', 'DoSpark')
	gamethread.delayed(0.2, es.fire, (userid, 'point_tesla', 'DoSpark'))
	gamethread.delayed(0.4, es.fire, (userid, 'point_tesla', 'DoSpark'))
	gamethread.delayed(0.6, es.fire, (userid, 'point_tesla', 'DoSpark'))
	gamethread.delayed(0.8, es.fire, (userid, 'point_tesla', 'DoSpark'))
	gamethread.delayed(1, es.fire, (userid, 'point_tesla', 'DoSpark'))
	gamethread.delayed(2, es.fire, (userid, 'point_tesla', 'Kill'))

def night():
	if dice <= 30:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'sprites/xbeam2.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 10, 10, 0, 255, 0, es.ServerVar('wcs_alpha'))
			effect.est_Effect(3, '#a', 0, 'sprites/hydraspinalcord.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 3, 3, 111, 244, 157, es.ServerVar('wcs_alpha'))

def bloodban():
	if dice <= 30:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'sprites/xbeam2.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 10, 10, 199, 255, 248, es.ServerVar('wcs_alpha'))
			effect.est_Effect(3, '#a', 0, 'sprites/hydraspinalcord.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 6, 6, 111, 244, 157, es.ServerVar('wcs_alpha'))

def bloodmana():
	if dice <= 30:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'sprites/yellowglow1.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 10, 10, 100, 255, 248, es.ServerVar('wcs_alpha'))

def bloodflame():
	if dice <= 30:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'sprites/c4.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 15, 15, 251, 255, 100, es.ServerVar('wcs_alpha'))
			effect.est_Effect(3, '#a', 0, 'sprites/crystal_beam1.vmt', v[0], v[1], v[2]+20, q[0], q[1], q[2]+20, 0.5, 10, 10, 232, 111, 0, es.ServerVar('wcs_alpha'))

def archmage():
	if dice <= 25:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			v[2] += 20
			q[2] += 20
			effect.est_Effect(3, '#a', 0, 'sprites/lgtning.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 15, 15, 251, 255, 100, 255)
			effect.est_Effect(3, '#a', 0, 'sprites/lgtning.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 5, 5, 251, 55, 200, 255)
			effect.est_Effect(3, '#a', 0, 'sprites/lgtning.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 20, 20, 163, 73, 164, 200)

def archmagespawn():
	if effect.EST:
		q = Vector(es.getplayerlocation(ev['userid']))
		effect.est_Effect(10, '#a', 0, 'sprites/scanner_dots2.vmt', q[0], q[1], q[2], 20, 400, 0.5, 40, 300, 1.8, 251, 55, 200, 255, 100)
		effect.est_Effect(10, '#a', 0, 'sprites/scanner_dots2.vmt', q[0], q[1], q[2]+30, 20, 400, 0.5, 40, 300, 1.8, 251, 55, 200, 255, 100)
		effect.est_Effect(10, '#a', 0, 'sprites/scanner_dots2.vmt', q[0], q[1], q[2]+60, 20, 400, 0.5, 40, 300, 1.8, 251, 55, 200, 255, 100)

def warden():
	if dice <= 25:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			v[2] += 20
			q[2] += 20
			effect.est_Effect(3, '#a', 0, 'sprites/scanner_dots2.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 15, 15, 251, 255, 100, 255)
			effect.est_Effect(3, '#a', 0, 'sprites/lgtning.vmt',       v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 5, 5, 251, 255, 0, 255)
			effect.est_Effect(3, '#a', 0, 'sprites/bluelaser1.vmt',    v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 20, 20, 163, 73, 164, 200)

def cryptshake():
	if dice <= chance:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			v[2] += 20
			q[2] += 20
			effect.est_Effect(3, '#a', 0, 'sprites/scanner_dots2.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 5, 5, 251, 255, 100, 255)
			effect.est_Effect(3, '#a', 0, 'sprites/plasmabeam.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 15, 15, 57, 202, 148, 255)
			effect.est_Effect(3, '#a', 0, 'sprites/plasma.vmt', v[0], v[1], v[2], q[0], q[1], q[2], 0.5, 2, 2, 255, 224, 4, 200)

def cryptdmg():
	if dice <= chance:
		if effect.EST:
			v = Vector(es.getplayerlocation(ev['attacker']))
			q = Vector(es.getplayerlocation(ev['userid']))
			effect.est_Effect(3, '#a', 0, 'effects/scanner_dots2.vmt', 0, 0, 9000, q[0], q[1], q[2], 1, 20, 11, 255, 255, 255, 255)
			effect.est_Effect(3, '#a', 0, 'effects/scanner_dots2.vmt', 0, 9000, 0, q[0], q[1], q[2], 1, 20, 11, 255, 255, 255, 255)
			effect.est_Effect(3, '#a', 0, 'effects/scanner_dots2.vmt', 9000, 0, 0, q[0], q[1], q[2], 1, 20, 11, 255, 255, 255, 255)
			effect.est_Effect(3, '#a', 0, 'effects/scanner_dots2.vmt', 1000, 0, 0, q[0], q[1], q[2], 1, 20, 11, 255, 255, 255, 255)
			effect.est_Effect(3, '#a', 0, 'effects/scanner_dots2.vmt', 0, 0, 999, q[0], q[1], q[2], 1, 20, 11, 255, 255, 255, 255)

			vec1 = ','.join(map(str, (v[0], v[1], v[2]+5)))
			vec2 = ','.join(map(str, q))

			effect.est_Effect_14('#a', 0, 'effects/blueflare1.vmt', vec2, vec1, 900, 2, 180)
			effect.est_Effect_14('#a', 0.1, 'effects/blueflare1.vmt', vec2, vec1, 900, 2, 35)
			effect.est_Effect_14('#a', 0, 'effects/blueflare1.vmt', vec2, vec1, 900, 2, 180)
			effect.est_Effect_14('#a', 0.1, 'effects/blueflare1.vmt', vec2, vec1, 900, 2, 65)
			effect.est_Effect_14('#a', 0, 'effects/blueflare1.vmt', vec2, vec1, 900, 2, 115)
			effect.est_Effect_14('#a', 0.1, 'effects/blueflare1.vmt', vec2, vec1, 900, 2, 45)

			effect.est_Effect_14('#a', 0.2, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 120)
			effect.est_Effect_14('#a', 0.3, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 100)
			effect.est_Effect_14('#a', 0.4, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 160)
			effect.est_Effect_14('#a', 0.5, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 130)
			effect.est_Effect_14('#a', 0.6, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 20)
			effect.est_Effect_14('#a', 0.7, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 50)
			effect.est_Effect_14('#a', 0.8, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 80)
			effect.est_Effect_14('#a', 0.9, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 140)
			effect.est_Effect_14('#a', 1.0, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 170)
			effect.est_Effect_14('#a', 1.1, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 150)
			effect.est_Effect_14('#a', 1.2, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 120)
			effect.est_Effect_14('#a', 1.3, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 110)
			effect.est_Effect_14('#a', 1.4, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 90)
			effect.est_Effect_14('#a', 1.5, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 70)
			effect.est_Effect_14('#a', 1.6, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 40)
			effect.est_Effect_14('#a', 1.7, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 10)
			effect.est_Effect_14('#a', 1.8, 'effects/yellowflare_noz.vmt', vec2, vec1, 900, 2, 30)

			effect.est_Effect_14('#a', 1.9, 'effects/blueblackflash.vmt', vec2, vec1, 900, 2, 32)
			effect.est_Effect_14('#a', 2.0, 'effects/blueblackflash.vmt', vec2, vec1, 900, 2, 36)
			effect.est_Effect_14('#a', 2.1, 'effects/blueblackflash.vmt', vec2, vec1, 900, 2, 43)
			effect.est_Effect_14('#a', 2.2, 'effects/blueblackflash.vmt', vec2, vec1, 900, 2, 102)

			effect.est_Effect_14('#a', 2.3, 'effects/redflare.vmt', vec2, vec1, 900, 2, 89)
			effect.est_Effect_14('#a', 2.4, 'effects/redflare.vmt', vec2, vec1, 900, 2, 99)
			effect.est_Effect_14('#a', 2.5, 'effects/redflare.vmt', vec2, vec1, 900, 2, 49)
			effect.est_Effect_14('#a', 2.6, 'effects/redflare.vmt', vec2, vec1, 900, 2, 79)
			effect.est_Effect_14('#a', 2.7, 'effects/redflare.vmt', vec2, vec1, 900, 2, 69)

def sccknifedmg():
	if effect.EST:
		v = Vector(es.getplayerlocation(ev['attacker']))
		q = Vector(es.getplayerlocation(ev['userid']))
		vec1 = ','.join(map(str, (v[0], v[1], v[2]+40)))
		vec2 = ','.join(map(str, q))
		effect.est_Effect_14('#a', 0, 'effects/muzzleflashX.vmt', vec2, vec1, 250, 25, 195)
		effect.est_Effect_08('#a', 0, 'effects/muzzleflashX.vmt', vec2, 20, 400, 1, 1, 90, 400, 0, 128, 64, 12, 255, 10, 1)
		effect.est_Effect_06('#a', 0, 'sprites/orangelight1.vmt', vec2, vec1, 100, 1, 1, 10, 10, 0, 255, 255, 255, 255, 50)

def flamespawn():
	if effect.EST:
		q = Vector(es.getplayerlocation(ev['userid']))
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+15, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+15, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+20, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+20, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+25, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+25, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+30, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+30, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+35, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+35, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+40, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+40, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+45, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+45, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+50, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+50, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+55, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+55, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+60, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/lgtning_noz.vmt', q[0], q[1], q[2]+60, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)

def camelonspawn():
	if effect.EST:
		q = Vector(es.getplayerlocation(ev['userid']))
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+15, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+15, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+20, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+20, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+25, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+25, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+30, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+30, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+35, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+35, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+40, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+40, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+45, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+45, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+50, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+50, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+55, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+55, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+60, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
		effect.est_Effect(10, '#a', 0, 'sprites/heatwave.vmt', q[0], q[1], q[2]+60, 80, 70, 6, 5, 15, 0, 255, 255, 255, 255, 255)
