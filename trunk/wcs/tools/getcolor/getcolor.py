import es
from cmdlib import registerServerCommand
from cmdlib import unregisterServerCommand
import playerlib
 
def load():
        registerServerCommand('wcs_getcolor', getcolor, '')
 
def unload():
        unregisterServerCommand('wcs_getcolor')
 
def getcolor(args):
        userid = int(args[0])
        var = str(args[1])
        var1 = str(args[2])
        var2 = str(args[3])
        var3 = str(args[4])
        player = playerlib.getPlayer(userid)
        color = player.getColor()
        a,b,c,d = color
        es.ServerVar(var).set(a)
        es.ServerVar(var1).set(b)
        es.ServerVar(var2).set(c)
        es.ServerVar(var3).set(d)