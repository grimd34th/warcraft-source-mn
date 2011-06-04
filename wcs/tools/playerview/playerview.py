# -*- coding:Utf-8 -*-
import es, playerviewlib


if not es.exists("command", "playerview"):
    es.regcmd("playerview", "wcs/tools/playerview/command", "playerview: get userid that player is aiming")

def command():
    # check count of argument
    if es.getargc() != 3: es.dbgmsg(0, 'Syntax: playerview <"entity" or "player"> <userid>')
    else:
        # get target type ("entity" or "player"), userid and viewplayer to execute
        target, userid, viewplayer = es.getargv(1), es.getargv(2), es.getargv(3)

        # if target is "entity"
        if target == "entity":
            # get index of entity that player is aiming
            player = playerviewlib.PlayerView(userid)
            player.entity()


        # if target is "player"
        elif target == "player":
            # get userid of player that player is aiming
    	    player = playerviewlib.PlayerView(userid)
            player.player()
	



	
        
