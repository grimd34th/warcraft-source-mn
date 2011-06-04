# Teleport Command
# By MiB
# wcs_teleport <userid> <xyz>
from es import entitysetvalue,getuserid,setplayerprop
from playerlib import getPlayer
from gamethread import delayedname,cancelDelayed
from wcs.logging import log
from cmdlib import registerServerCommand,unregisterServerCommand

def load():
    registerServerCommand("wcs_teleport",Register,"")

def unload():
    unregisterServerCommand("wcs_teleport")

def Exists(userid):
    return getuserid(userid)

def Register(args):
    if len(args) == 2:
        if Exists(args[0]):
            player = getPlayer(args[0])
            if not player.isdead:
                entitysetvalue(player.index,"origin"," ".join(args[1].split(",")))
                loc = player.location
                players = player.getNearPlayers(128)
                if len(players):
                    for userid in players:
                        pl = getPlayer(userid)
                        oldno = pl.noblock
                        pl.noblock(1)
                        name = "pushtele_%s"%userid
                        cancelDelayed(name)
                        delayedname(.2,name,pl.noblock,(oldno))
                        oldno = player.noblock
                    player.noblock(1)
                    name = "pushtele_%s"%args[0]
                    cancelDelayed(name)
                    delayedname(.2,name,player.noblock,(oldno))
                    setplayerprop(args[0],"CBasePlayer.localdata.m_vecBaseVelocity","260.00000,0,15")
            else:
                log("Got: wcs_teleport " + " ".join(map(str,args)) + ".")
                log("Information: Userid is dead.")
        else:
            log("Got: wcs_teleport " + " ".join(map(str,args)) + ".")
            log("Information: Unknown userid.")
    else:
        log("Got: wcs_teleport " + " ".join(map(str,args)) + ".")
        log("Information: Got too many or too little arguments.")
