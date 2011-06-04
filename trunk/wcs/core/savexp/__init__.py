import wcs



def doCommand(userid, tell=True):
	userid = str(userid)
	if userid in wcs.wcs.tmp:
		tmp[userid].save()
	if userid in wcs.wcs.tmp1:
		tmp1[userid].save()
	if userid in wcs.wcs.tmp2:
		for x in tmp2[userid]:
			tmp2[userid].save()

	if tell:
		wcs.wcs.tell(userid, 'savexp: saved')
