import urllib
import database

		
def instructions(keys,dbport):
	from utilities import getArtistInfo
	from htmlgenerators import clean, artistLink, artistLinks, KeySplit
	from htmlmodules import module_pulse, module_trackcharts

	filterkeys, _, _, _ = KeySplit(keys,forceArtist=True)
	info = getArtistInfo(filterkeys["artist"])
	imgurl = info.get("image")
	pushresources = [{"file":imgurl,"type":"image"}] if imgurl.startswith("/") else []
	
	data = database.artistInfo(filterkeys["artist"])
	scrobbles = str(data["scrobbles"])
	pos = "#" + str(data["position"])
	
	credited = data.get("replace")
	includestr = " "
	if credited is not None:
		includestr = "Competing under " + artistLink(credited) + " (" + pos + ")"
		pos = ""
	included = data.get("associated")
	if included is not None and included != []:
		includestr = "associated: "
		includestr += artistLinks(included)
	

	html_tracks, _ = module_trackcharts(**filterkeys,max_=15)	
	
	
	html_pulse = module_pulse(**filterkeys,step="year",stepn=1,trail=1)

	replace = {"KEY_ARTISTNAME":keys["artist"],"KEY_ENC_ARTISTNAME":urllib.parse.quote(keys["artist"]),
	"KEY_IMAGEURL":imgurl, "KEY_DESCRIPTION":"",
	"KEY_TRACKLIST":html_tracks,"KEY_PULSE":html_pulse,
	"KEY_SCROBBLES":scrobbles,"KEY_POSITION":pos,
	"KEY_ASSOCIATED":includestr}
	
	return (replace,pushresources)
