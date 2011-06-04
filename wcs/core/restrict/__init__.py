import es
import wcs
 
import spe
 
from UserDict import UserDict
 
class cRestrict(UserDict):
        def __init__(self, data = {}, **kw):
                UserDict.__init__(self)
 
        def restrict(self, userid, weapon):
                userid = str(userid)
                if es.exists('userid', userid):
                        weapon = weaponw(weapon)
                        if not userid in self.data:
                                self.data[userid] = {}
 
                        remove(userid, weapon)
 
                        if not weapon in self.data[userid]:
                                self.data[userid][weapon] = 0
 
                        self.data[userid][weapon] += 1
 
        def allow(self, userid, weapon):
                userid = str(userid)
                if es.exists('userid', userid):
                        weapon = weaponw(weapon)
                        if not userid in self.data:
                                self.data[userid] = {}
 
                        if not weapon in self.data[userid]:
                                self.data[userid][weapon] = 1
 
                        self.data[userid][weapon] -= 1
 
                        if not self.data[userid][weapon]:
                                self.data[userid].__delitem__(weapon)
restrictData = cRestrict()
 
def restrict(userid, weapon):
        restrictData.restrict(userid, weapon)
 
def allow(userid, weapon):
        restrictData.allow(userid, weapon)
 
def weaponw(weapon):
        return str(weapon).lower().replace('weapon_', '')
 
def remove(userid, weapon):
        longname = 'weapon_'+weaponw(weapon)
        if es.createplayerlist(userid)[int(userid)]['weapon'] == longname:
                es.cexec(userid, 'lastinv')
 
        handle = es.getplayerhandle(userid)
        for index in es.createentitylist(longname):
                if es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity') <> handle:
                        continue
 
                spe.dropWeapon(userid, longname)
 
                wcs.wcs.tell(userid, 'xrestrict: restricted')
                break