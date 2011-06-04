import es
import gamethread
from wcs.core.expand import give


class EffectManager(object):
	def __init__(self):
		self.unique = 0
		self.userid = 0
		self.index = es.ServerVar('eventscripts_lastgive')
		self.EST = False
		self.SPE = False
		self.NT = False

	class CommandProxy(object):
		def __init__(self, name):
			self.name = name

		def __call__(self, *args):
			execute = []
			execute.append(self.name)
			for arg in args:
				if isinstance(arg, es.ServerVar):
					execute.append(arg.getName)
				else:
					execute.append(arg)

			es.server.insertcmd(' '.join(map(str, execute)))

	def __getattr__(self, attr):
		#if hasattr(self, attr):
		#	return getattr(self, attr)

		if self.EST and es.exists('command', attr):
			return self.CommandProxy(attr)

		elif self.SPE and hasattr(spe, attr):
			return getattr(spe, attr)

		elif self.NT and hasattr(nt, attr):
			return getattr(nt, attr)

		raise AttributeError, "EffectManager instance has no attribute '"+str(attr)+"'"

	def BlueCircle(self, origin,
								 BaseSpread=70,
								 SpreadSpeed=10,
								 Initial=0,
								 Speed=10,
								 StartSize=1,
								 EndSize=7,
								 Rate=350,
								 JetLength=13,
								 RenderColor=(0,0,200),
								 RenderMode=0,
								 RenderAmt=200,
								 SmokeMaterial='effects\combinemuzzle2.vmt',
								 Angles=(0,0,0),
								 Twist=0,
								 Delayed=0,
								 Name='BlueCircle',
								 Userid=None):

		self.fire(origin, BaseSpread, SpreadSpeed, Initial, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name, Userid)

	#Thanks to Kami
	def RedCircle(self, origin,
								BaseSpread=30,
								SpreadSpeed=50,
								Initial=0,
								Speed=60,
								StartSize=5,
								EndSize=10,
								Rate=15,
								JetLength=999,
								RenderColor=(250,0,0),
								RenderMode=0,
								RenderAmt=255,
								SmokeMaterial='effects/bluemuzzle.vmt',
								Angles=(0,0,0),
								Twist=999,
								Delayed=0,
								Name='RedCircle',
								Userid=None):

		self.fire(origin, BaseSpread, SpreadSpeed, Initial, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name, Userid)

	def Bubble(self, origin,
							 BaseSpread=10,
							 SpreadSpeed=15,
							 Initial=0,
							 Speed=6,
							 StartSize=15,
							 EndSize=150,
							 Rate=4,
							 JetLength=330,
							 RenderColor=(200,0,0),
							 RenderMode=0,
							 RenderAmt=255,
							 SmokeMaterial='effects/bubble.vmt',
							 Angles=(0,0,0),
							 Twist=20,
							 Delayed=0,
							 Name='Bubble',
							 Userid=None):

		self.fire(origin, BaseSpread, SpreadSpeed, Initial, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name, Userid)

	#Thanks to Psycho
	def Bubble1(self, origin,
						   BaseSpread=14,
						   SpreadSpeed=5,
						   Initial=0,
						   Speed=30,
						   StartSize=1,
						   EndSize=5,
						   Rate=50,
						   JetLength=100,
						   RenderColor=(5,255,158),
						   RenderMode=0,
						   RenderAmt=255,
						   SmokeMaterial='sprites/strider_blackball.vmt',
						   Angles=(0,0,0),
						   Twist=0,
						   Delayed=0,
						   Name='Bubble1',
						   Userid=None):

		self.fire(origin, BaseSpread, SpreadSpeed, Initial, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name, Userid)

	#Thanks to Avast
	def Pyramide(self, origin,
						   BaseSpread=15,
						   SpreadSpeed=100,
						   Initial=0,
						   Speed=50,
						   StartSize=15,
						   EndSize=25,
						   Rate=200,
						   JetLength=100,
						   RenderColor=(100,100,220),
						   RenderMode=0,
						   RenderAmt=255,
						   SmokeMaterial='particle/fire.vmt',
						   Angles=(0,0,0),
						   Twist=5,
						   Delayed=0,
						   Name='Bubbles',
						   Userid=None):

		self.fire(origin, BaseSpread, SpreadSpeed, Initial, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name, Userid)

	#Thanks to HOLLIDAY
	def Ground(self, origin,
							 BaseSpread=15,
							 SpreadSpeed=30,
							 Initial=0,
							 Speed=60,
							 StartSize=5,
							 EndSize=1,
							 Rate=200,
							 JetLength=175,
							 RenderColor=(100,100,220),
							 RenderMode=0,
							 RenderAmt=100,
							 SmokeMaterial='particle/fire.vmt',
							 Angles=(0,0,0),
							 Twist=175,
							 Delayed=0,
							 Name='Ground',
							 Userid=None):

		self.fire(origin, BaseSpread, SpreadSpeed, Initial, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name, Userid)

	def Trail(self, userid,
							BaseSpread=5,
							SpreadSpeed=10,
							Speed=10,
							StartSize=5,
							EndSize=1,
							Rate=200,
							JetLength=100,
							RenderColor=(150,50,200),
							RenderMode=18,
							RenderAmt=100,
							SmokeMaterial='particle/fire.vmt',
							Angles=(0,0,0),
							Twist=5,
							Delayed=0,
							Name='Trail'):

		self.fire1(userid, BaseSpread, SpreadSpeed, Speed, StartSize, EndSize, Rate, JetLength, RenderColor, RenderMode, RenderAmt, SmokeMaterial, Angles, Twist, Delayed, Name)

	def Explosion(self, origin,
								IMagniTude=400,
								IRadiusOverride=150,
								FireBallSprite='sprites/ar2_muzzle1.vmt',
								RenderMode=18,
								HOwner=None,
								Name='Explosion'):

		if self.getUserid() and origin:
			#index = es.createentity('env_explosion', Name+str(self.unique))
			index = spe.getEntityIndex(spe.createEntity('env_explosion'))
			es.entitysetvalue(index, 'targetname', self.getUserid())
			#es.entcreate(self.getUserid(), 'env_explosion')
			#index = str(es.ServerVar('eventscripts_lastgive'))
			es.entitysetvalue(index, 'origin', ' '.join(map(str, origin)))
			es.entitysetvalue(index, 'imagnitude', IMagniTude)
			es.entitysetvalue(index, 'iradiusoverride', IRadiusOverride)
			if HOwner is not None:
				es.setindexprop(index, 'CBaseEntity.m_hOwnerEntity', HOwner)

			es.fire(self.userid, Name+str(self.unique), 'explode')
			es.fire(self.userid, Name+str(self.unique), 'Kill')
			self.unique += 1


	#Helper functions:
	def kill(self, entity):
		if self.getUserid():
			es.fire(self.userid, entity, 'TurnOff')
			es.fire(self.userid, entity, 'Kill')

	def getUserid(self):
		self.userid = es.getuserid()
		return self.userid

	def fire(self, origin,
						   BaseSpread,
						   SpreadSpeed,
						   Initial,
						   Speed,
						   StartSize,
						   EndSize,
						   Rate,
						   JetLength,
						   RenderColor,
						   RenderMode,
						   RenderAmt,
						   SmokeMaterial,
						   Angles,
						   Twist,
						   Delayed,
						   Name,
						   Userid):
		if self.getUserid() and origin:
			#index = es.createentity('env_smokestack', Name+str(self.unique))
			index = spe.getEntityIndex(spe.createEntity('env_smokestack'))
			es.entitysetvalue(index, 'targetname', self.getUserid())
			#es.entcreate(self.getUserid(), 'env_smokestack')
			#index = str(es.ServerVar('eventscripts_lastgive'))
			es.entitysetvalue(index, 'Origin', ' '.join(map(str, origin)))
			es.entitysetvalue(index, 'BaseSpread', BaseSpread)
			es.entitysetvalue(index, 'SpreadSpeed', SpreadSpeed)
			es.entitysetvalue(index, 'Initial', Initial)
			es.entitysetvalue(index, 'Speed', Speed)
			es.entitysetvalue(index, 'StartSize', StartSize)
			es.entitysetvalue(index, 'EndSize', EndSize)
			es.entitysetvalue(index, 'Rate', Rate)
			es.entitysetvalue(index, 'JetLength', JetLength)
			es.entitysetvalue(index, 'RenderColor', ' '.join(map(str, RenderColor)))
			es.entitysetvalue(index, 'RenderMode', RenderMode)
			es.entitysetvalue(index, 'RenderAmt', RenderAmt)
			es.entitysetvalue(index, 'SmokeMaterial', SmokeMaterial)
			es.entitysetvalue(index, 'Angles', ' '.join(map(str, Angles)))
			es.entitysetvalue(index, 'Twist', Twist)
			es.spawnentity(index)
			if Userid is not None:
				#es.entitysetvalue(index, 'Parent',
				#es.fire(self.userid, Name+str(self.unique), 'SetParent', Userid)
				es.fire(Userid, Name+str(self.unique), 'SetParent', '!activator')
			es.fire(self.userid, Name+str(self.unique), 'TurnOn')
			if Delayed:
				gamethread.delayed(float(Delayed), self.kill, Name+str(self.unique))
			self.unique += 1

	def fire1(self, userid,
						   BaseSpread,
						   SpreadSpeed,
						   Speed,
						   StartSize,
						   EndSize,
						   Rate,
						   JetLength,
						   RenderColor,
						   RenderMode,
						   RenderAmt,
						   SmokeMaterial,
						   Angles,
						   Twist,
						   Delayed,
						   Name):
		if self.getUserid() and es.exists('userid', userid):
			give(userid, 'env_smokestack')
			es.entitysetvalue(str(self.index), 'TargetName', Name+str(self.unique))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'BaseSpread '+str(BaseSpread))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'SpreadSpeed '+str(SpreadSpeed))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'Initial 0')
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'Speed '+str(Speed))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'StartSize '+str(StartSize))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'EndSize '+str(EndSize))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'Rate '+str(Rate))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'JetLength '+str(JetLength))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'RenderColor '+str(' '.join(map(str, RenderColor))))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'RenderMode '+str(RenderMode))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'RenderAmt '+str(RenderAmt))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'SmokeMaterial '+str(SmokeMaterial))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'Angles '+str(' '.join(map(str, Angles))))
			es.fire(userid, Name+str(self.unique), 'AddOutPut', 'Twist '+str(Twist))
			es.fire(userid, Name+str(self.unique), 'TurnOn')
			es.fire(userid, Name+str(self.unique), 'setparent', '!activator')
			if Delayed:
				gamethread.delayed(float(Delayed), self.kill, Name+str(self.unique))
			self.unique += 1
effect = EffectManager()

if bool(es.ServerVar('wcs_effects')):
	effect.EST = True
	es.ServerVar('wcs_isest').set(1)
else:
	effect.EST = False
	es.ServerVar('wcs_isest').set(0)

try:
	import spe
	effect.SPE = True
	es.ServerVar('wcs_isspe').set(1)
except ImportError:
	effect.SPE = False
	es.ServerVar('wcs_isspe').set(0)

try:
	import nativetools as nt
	effect.NT = True
	es.ServerVar('wcs_isnt').set(1)
except ImportError:
	effect.NT = False
	es.ServerVar('wcs_isnt').set(0)
