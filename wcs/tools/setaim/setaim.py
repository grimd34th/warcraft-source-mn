# SetAim Command
# By MiB
# wcs_setaim <userid> <target> <z add>
from es import getplayerlocation,getuserid,createvectorstring,createvectorfrompoints,splitvectorstring,server
from playerlib import getPlayer
from math import atan,degrees,sqrt,pow as powm
from wcs.logging import log
from cmdlib import registerServerCommand,unregisterServerCommand

def load():
    registerServerCommand("wcs_setaim",Register,"")

def unload():
    unregisterServerCommand("wcs_setaim")

def Exists(userid):
    return getuserid(userid)

def viewCoord(userid,value):
    '''Credit goes to the people who made this for playerlib, I just tweaked a few things'''
    player = getPlayer(userid)
    myLocation = player.getEyeLocation()
    myVector = createvectorstring(myLocation[0], myLocation[1], myLocation[2])
    theVector = createvectorstring(value[0], value[1], value[2])
    ourVector = createvectorfrompoints(myVector, theVector)
    ourVector = splitvectorstring(ourVector)
    myViewAngle = player.getViewAngle()
    ourAtan = degrees(atan(float(ourVector[1]) / float(ourVector[0])))
    if float(ourVector[0]) < 0:
        RealAngle = ourAtan + 180
    elif float(ourVector[1]) < 0:
        RealAngle = ourAtan + 360
    else:
        RealAngle = ourAtan
    yAngle = RealAngle
    xAngle = 0 - degrees(atan(ourVector[2] / sqrt(powm(float(ourVector[1]), 2) + powm(float(ourVector[0]), 2))))
    server.queuecmd("es_xsetang %s %s %s %s"%(userid,xAngle,yAngle,myViewAngle[2]))

def Register(args):
    if len(args) == 3:
        if Exists(args[0]):
            if not getPlayer(args[0]).isdead:
                if Exists(args[1]):
                    x,y,z = getplayerlocation(args[1])
                    z += float(args[2])
                    viewCoord(args[0],(x,y,z))
                else:
                    log("Got: wcs_setaim " + " ".join(map(str,args)) + ".")
                    log("Information: Unknown target.")
            else:
                log("Got: wcs_setaim " + " ".join(map(str,args)) + ".")
                log("Information: Userid is dead.")
        else:
            log("Got: wcs_setaim " + " ".join(map(str,args)) + ".")
            log("Information: Unknown userid.")
    else:
        log("Got: wcs_setaim " + " ".join(map(str,args)) + ".")
        log("Information: Got too many or too little arguments.")
