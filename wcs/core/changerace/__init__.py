import es
from popuplib import create, send
import playerlib
import wcs
 
popups = []
 
def doCommand(userid, args='changerace', msg=True):
   if es.exists('userid', userid):
      if args == 'changerace':
         args = 'changerace7'
 
      positionsearch = str(args.replace('changerace', '').strip())
 
      if len(positionsearch):
         if positionsearch.isdigit():
            positionsearch = int(positionsearch)
         else:
            positionsearch = 7
      else:
         positionsearch = 7
 
      races = wcs.wcs.racedb.getAll()
 
      #allraces = sorted(races, key=lambda x: races[x]['required'], reverse=False)
      allraces = races.keys()
 
      del allraces[:positionsearch - 7]
      del allraces[positionsearch:]
 
      if len(allraces):
         pname = 'changerace_%s_%s'%(userid, positionsearch)
         popups.append(pname)
         changerace = create(pname)
 
         changerace.addline('Please choose a race')
 
         changerace.addline(' ')
         changerace.menuselect = callBack
 
         player = wcs.wcs.getPlayer(userid)
 
         totallevel = player.player.totallevel
 
         added = 0
         for number, race in enumerate(allraces):
            if number < 7:
               added += 1
               v = canUse(userid, race)
               raceinfo = wcs.wcs.racedb.getRace(race)
               team = es.getplayerteam(userid)
               if not v:
                  if wcs.wcs.showracelevel:
                     level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                  else:
                     level = 0
                  changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
               elif v == 1:
                  if team in (2,3):
                     team = {2:'T',3:'CT'}[team]
 
                     changerace.addline(str(number+1)+'. '+str(race)+' (teamlimit '+raceinfo['teamlimit']+')')
                     changerace.submenu(number+1, pname)
                  else:
                     if wcs.wcs.showracelevel:
                        level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                     else:
                        level = 0
                     changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
                  '''if wcs.wcs.showracelevel:
                     level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                  else:
                     level = 0
                  changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))'''
               elif v == 2:
                  changerace.addline(str(number+1)+'. '+str(race)+' (maximum level '+str(raceinfo['maximum'])+')')
                  changerace.submenu(number+1, pname)
               elif v == 3:
                  changerace.addline(str(number+1)+'. '+str(race)+' (minimum level '+raceinfo['required']+')')
                  changerace.submenu(number+1, pname)
               elif v == 4:
                  if team in (2,3):
                     changerace.addline(str(number+1)+'. '+str(race)+' (restricted team '+{2:'T',3:'CT'}[team]+')')
                     changerace.submenu(number+1, pname)
                  else:
                     if wcs.wcs.showracelevel:
                        level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                     else:
                        level = 0
                     changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
               elif v == 5:
                  changerace.addline(str(number+1)+'. '+str(race)+' (private race)')
                  changerace.submenu(number+1, pname)
               elif v == 6:
                  changerace.addline(str(number+1)+'. '+str(race)+' (restricted map '+wcs.wcs.curmap+')')
                  changerace.submenu(number+1, pname)
               '''raceinfo = wcs.wcs.racedb.getRace(race)
 
               if not wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
                  admins = raceinfo['allowonly'].split('|')
                  if len(admins) == 1 and not admins[0]:
                     del admins[0]
 
                  if not len(admins) or len(admins) and (es.getplayersteamid(userid) in admins or 'ADMINS' in admins) and es.getplayersteamid(userid) in wcs.wcs.admin.admins:
                     team = int(es.getplayerteam(userid))
                     if not raceinfo['restrictteam'] or not int(raceinfo['restrictteam']) == team:
                        if totallevel >= int(raceinfo['required']):
                           if int(raceinfo['maximum']) and totallevel <= int(raceinfo['maximum']):
                              changerace.addline(''+str(number+1)+'. '+str(race)+' (maximum level '+str(raceinfo['maximum'])+')')
                              changerace.submenu(number+1, pname)
                           else:
                              changerace.addline('->'+str(number+1)+'. '+str(race))
                        else:
                           changerace.addline(''+str(number+1)+'. '+str(race)+' (minimum level '+raceinfo['required']+')')
                           changerace.submenu(number+1, pname)
                     else:
                        changerace.addline(''+str(number+1)+'. '+str(race)+' (restricted team '+{2:'T',3:'CT'}[team]+')')
                        changerace.submenu(number+1, pname)
                  else:
                     changerace.addline(''+str(number+1)+'. '+str(race)+' (private race)')
                     changerace.submenu(number+1, pname)
               else:
                  changerace.addline(''+str(number+1)+'. '+str(race)+' (restricted map '+wcs.wcs.curmap+')')
                  changerace.submenu(number+1, pname)'''
            else:
               break
 
         while added < 7:
            changerace.addline(' ')
            added += 1
            changerace.submenu(added, pname)
 
         changerace.addline(' ')
         if positionsearch < 8:
            changerace.addline(' ')
            changerace.submenu(8, pname)
         else:
            changerace.addline('->8. Back')
 
         if len(races.keys()) < positionsearch+1:
            changerace.addline(' ')
            changerace.submenu(9, pname)
         else:
            changerace.addline('->9. Next')
 
         changerace.addline('0. Close')
 
         if positionsearch == 7:
            if msg:
               wcs.wcs.tell(userid, 'changerace: still alive')
 
         changerace.send(userid)
         es.ServerVar('wcs_ppuser').set(userid)
         es.doblock("wcs/tools/pending/pending")
 
 
def popupHandler(userid, choice, popupid):
   if es.exists('userid', userid):
      last_split  = popupid.split('_')
      last_search = int(last_split[2])
 
      races = wcs.wcs.racedb.getAll()
 
      if choice == 8:
         if last_search < 0:
            doCommand(userid, 'changerace7')
 
         elif last_search < 6:
            send(popupid, userid)
 
         else:
            newsearch = int(last_search)-7
            doCommand(userid, 'changerace%s'%newsearch, False)
 
      elif choice == 9:
         #if last_search >= len(races.keys()):
         #   send(popupid, userid)
 
         #else:
         if last_search < len(races.keys()):
            newsearch = int(last_search)+7
            doCommand(userid, 'changerace%s'%newsearch, False)
 
      elif choice < 8:
         race_select = choice-1
         #race_select = divmod(last_search, 7)[0]*7-(8-choice) #Find the number where the race is placed
 
         #allraces = sorted(races, key=lambda x: races[x]['required'], reverse=False)
         allraces = races.keys()
 
         del allraces[:last_search - 7]
         del allraces[last_search:]
 
         try:
            player = wcs.wcs.getPlayer(userid)
            totallevel = player.player.totallevel
 
            race = allraces[race_select]
            raceinfo = wcs.wcs.racedb.getRace(race)
            team = int(es.getplayerteam(userid))
            teamlimit = raceinfo['teamlimit']
            admins = raceinfo['allowonly'].split('|')
         
            if len(admins) == 1 and not admins[0]:
               del admins[0]
 
            if wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
               wcs.wcs.tell(userid, 'changerace: restricted map', {'race':race, 'map':wcs.wcs.curmap})
 
            #elif len(admins) and (es.getplayersteamid(userid) not in admins or 'ADMINS' in admins) and not es.getplayersteamid(userid) in wcs.wcs.admin.admins:
	    elif len(admins) and (es.getplayersteamid(userid) not in admins or ('ADMINS' in admins and es.getplayersteamid(userid) not in admins)) and (es.getplayersteamid(userid) not in wcs.wcs.admin.admins):
               wcs.wcs.tell(userid, 'changerace: restricted player', {'race':race})
 
            elif int(raceinfo['restrictteam']) and int(raceinfo['restrictteam']) == team:
               wcs.wcs.tell(userid, 'changerace: restricted team', {'race':race, 'team':{2:'T',3:'CT'}[team]})
 
            elif totallevel < int(raceinfo['required']):
               diffience = str(int(raceinfo['required'])-int(player.player.totallevel))
               wcs.wcs.tell(userid, 'changerace: required level', {'race':race, 'diffience':diffience})
 
            elif int(raceinfo['maximum']) and totallevel > int(raceinfo['maximum']):
               diffience = str(int(player.player.totallevel)-int(raceinfo['maximum']))
               wcs.wcs.tell(userid, 'changerace: high level', {'race':race, 'diffience':diffience})
 
            elif team in (2,3) and 'teamlimit' in raceinfo and len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == es.getplayerteam(userid), es.getUseridList()))) >= int(raceinfo['teamlimit']) and not int(raceinfo['teamlimit']) == 0:
               wcs.wcs.tell(userid, 'changerace: team limit', {'race':race, 'teamlimit' :teamlimit})
 
            else:
               wcs.wcs.tell(userid, 'changerace: change race', {'race':race})
               player.changeRace(race)
 
               wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
 
               #keydelete('WCSuserdata', userid)
               #keycreate('WCSuserdata', userid)
               #wcs.wcs.wcsgroup.delUser(userid)
               #wcs.wcs.wcsgroup.addUser(userid)
         except IndexError:
            pass
 
def canUse(userid, race):
   raceinfo = wcs.wcs.racedb.getRace(race)
 
   if not wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
      admins = raceinfo['allowonly'].split('|')
      #if len(admins) == 1 and not admins[0]:
      #   del admins[0]
 
      #if len(admins) and (es.getplayersteamid(userid) not in admins or 'ADMINS' in admins) and not es.getplayersteamid(userid) in wcs.wcs.admin.admins
      #if not len(admins) or len(admins) and (es.getplayersteamid(userid) in admins or 'ADMINS' in admins) and es.getplayersteamid(userid) in wcs.wcs.admin.admins:
      if (len(admins) and not admins[0]) or (es.getplayersteamid(userid) in admins) or ('ADMINS' in admins and es.getplayersteamid(userid) in wcs.wcs.admin.admins):
         team = int(es.getplayerteam(userid))
         if not raceinfo['restrictteam'] or not int(raceinfo['restrictteam']) == team:
            totallevel = wcs.wcs.getPlayer(userid).player.totallevel
            if totallevel >= int(raceinfo['required']):
               if int(raceinfo['maximum']) and totallevel > int(raceinfo['maximum']):
                  return 2
               else:
                  if team in (2,3) and len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == es.getplayerteam(userid), es.getUseridList()))) >= int(raceinfo['teamlimit']) and not int(raceinfo['teamlimit']) == 0:
                     return 1
 
                  return 0
            return 3
         return 4
      return 5
   return 6
 
 
callBack = popupHandler
 
def getPopups():
   return popups