# Random Player Command
# By MiB
# wcs_randplayer <return variable> <flags>
# flags = ["#alive","#all","#bot","#ct","#dead","#human","#spec","#t","#un"]
from es import ServerVar
from wcs.logging import log
from cmdlib import registerServerCommand,unregisterServerCommand
from playerlib import getPlayerList
from random import choice

def load():
    registerServerCommand("wcs_randplayer",Register,"")

def unload():
    unregisterServerCommand("wcs_randplayer")

def Register(args):
    if len(args) == 2:
        try:
            ServerVar(args[0]).set(choice(getPlayerList(args[1])))
        except IndexError:
            ServerVar(args[0]).set(0)
    else:
        log("Got: wcs_randplayer " + " ".join(map(str,args)) + ".")
        log("Information: Got too many or too little arguments.")
