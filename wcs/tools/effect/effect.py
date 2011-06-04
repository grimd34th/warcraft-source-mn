import es
import cmdlib
from wcs import wcs


def load():
	cmdlib.registerServerCommand('wcs_effect', register, '')

def unload():
	cmdlib.unregisterServerCommand('wcs_effect')

def register(args):
	if len(args) > 1:
		todo = str(args[0])

		if todo == 'bluecircle':
			if len(args) == 23:
				wcs.effect.effect.BlueCircle((args[1],args[2],args[3]),args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],(args[12],args[13],args[14]),
				args[15],args[16],args[17],(args[18],args[19],args[20]),args[21],args[22])
			else:
				wcs.logging.log('effect: Error: Syntax: wcs_effect bluecircle <x> <y> <z> <basespread> <spreadspeed> <initial> <speed> <startsize> <endsize> <rate> \
<jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
				wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

		elif todo == 'redcircle':
			if len(args) == 23:
				wcs.effect.effect.RedCircle((args[1],args[2],args[3]),args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],(args[12],args[13],args[14]),
				args[15],args[16],args[17],(args[18],args[19],args[20]),args[21],args[22])
			else:
				wcs.logging.log('effect: Error: Syntax: wcs_effect redcircle <x> <y> <z> <basespread> <spreadspeed> <initial> <speed> <startsize> <endsize> <rate> \
<jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
				wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

		elif todo == 'bubble':
			if len(args) == 23:
				wcs.effect.effect.Bubble((args[1],args[2],args[3]),args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],(args[12],args[13],args[14]),
				args[15],args[16],args[17],(args[18],args[19],args[20]),args[21],args[22])
			else:
				wcs.logging.log('effect: Error: Syntax: wcs_effect bubble <x> <y> <z> <basespread> <spreadspeed> <initial> <speed> <startsize> <endsize> <rate> \
<jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
				wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

		elif todo == 'bubble1':
			if len(args) == 23:
				wcs.effect.effect.Bubble1((args[1],args[2],args[3]),args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],(args[12],args[13],args[14]),
				args[15],args[16],args[17],(args[18],args[19],args[20]),args[21],args[22])
			else:
				wcs.logging.log('effect: Error: Syntax: wcs_effect bubble1 <x> <y> <z> <basespread> <spreadspeed> <initial> <speed> <startsize> <endsize> <rate> \
<jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
				wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

		elif todo == 'pyramide':
			if len(args) == 23:
				wcs.effect.effect.Pyramide((args[1],args[2],args[3]),args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],(args[12],args[13],args[14]),
				args[15],args[16],args[17],(args[18],args[19],args[20]),args[21],args[22])
			else:
				wcs.logging.log('effect: Error: Syntax: wcs_effect pyramide <x> <y> <z> <basespread> <spreadspeed> <initial> <speed> <startsize> <endsize> <rate> \
<jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
				wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

		elif todo == 'ground':
			if len(args) == 23:
				wcs.effect.effect.Ground((args[1],args[2],args[3]),args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],(args[12],args[13],args[14]),
				args[15],args[16],args[17],(args[18],args[19],args[20]),args[21],args[22])
			else:
				wcs.logging.log('effect: Error: Syntax: wcs_effect ground <x> <y> <z> <basespread> <spreadspeed> <initial> <speed> <startsize> <endsize> <rate> \
<jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
				wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

		else:
			wcs.logging.log('effect: Error: Unknown sub-command: '+todo)
			wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))

	else:
		wcs.logging.log('effect: Error: Syntax: wcs_effect <bluecircle/redcircle/bubble/bubble1/pyramide/ground> <x> <y> <z> <basespread> <spreadspeed> <initial> \
<speed> <startsize> <endsize> <rate> <jetlength> <red> <green> <blue> <mode> <amt> <material> <pitch> <yaw> <roll> <twist> <time>')
		wcs.logging.log('effect: Information: Got: wcs_effect '+' '.join(map(str, args)))
