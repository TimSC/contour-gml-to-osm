import bz2, os
import xml.etree.ElementTree as ET
from ostn02python import OSGB, OSTN02

def MergeFile(fina, ty, nextObjId, idMapping, fiOut):
	fi = bz2.BZ2File(fina)
	root = ET.fromstring(fi.read())

	if fina not in idMapping:
		idMapping[fina] = {}
	fiMapping = idMapping[fina]

	if ty not in fiMapping:
		fiMapping[ty] = {}
	tyMapping = fiMapping[ty]
	ndMapping = fiMapping['node']

	for el in root:
		if el.tag != ty: continue
		oldId = el.attrib['id']
		tyMapping[oldId] = str(nextObjId[ty])
		nextObjId[ty] -= 1

		el.attrib['id'] = tyMapping[oldId]
		print el.tag, el.attrib['id']

		for ch in el:
			if ch.tag=="nd":
				#print ch.tag, ch.attrib
				#print "Remap node", ch.attrib['ref'], "to", ndMapping[ch.attrib['ref']]
				ch.attrib['ref'] = ndMapping[ch.attrib['ref']]
			if ch.tag=="member":
				assert(0)#Not implemented

		xml = ET.tostring(el, encoding="utf-8")
		fiOut.write(xml)

if __name__=="__main__":
	
	out = bz2.BZ2File("merge.osm.bz2","w")
	#out = open("merge.osm","wt")
	out.write("<?xml version='1.0' encoding='UTF-8'?>\n")
	out.write("<osm version='0.6' upload='true' generator='py'>\n")

	#lats, lons = [51.383075,50.50], [-1.955713,-0.729294] #Hampshire
	#lats, lons = [50.703, 51.167], [-0.955, 0.040] #West sussex
	#lats, lons = [50.7217072, 51.1475977], [-0.1424041, 0.8675128]  #East sussex
	lats, lons = [51.8251473, 52.3967369], [-3.1446227, -2.3441835]  #Herefordshire

	collectEastings = []
	collectNorthings = []

	#Convert to OS grid
	for lat in lats:
		for lon in lons:
			
			(x2,y2) = OSGB.ll_to_grid(lat, lon)
			try:
				e, n, h = OSTN02.ETRS89_to_OSGB36(x2,y2,0.)
			except:
				print "Error: OSTN02 not defined here, using approximation"
				e, n, h = x2, y2, 0.
	
			print e, n, OSGB.grid_to_os_streetview_tile((e, n))
			collectEastings.append(e)
			collectNorthings.append(n)

	#Convert to rectangular area
	minE = min(collectEastings)
	minN = min(collectNorthings)
	minE = int(round(minE - (minE % 10000)))
	minN = int(round(minN - (minN % 10000)))

	maxE = max(collectEastings)
	maxN = max(collectNorthings)
	maxE = int(round(maxE - (maxE % 10000) + 10000))
	maxN = int(round(maxN - (maxN % 10000) + 10000))
	print "e", minE, maxE
	print "n", minN, maxN

	fiList = []
	for e in range(minE, maxE+10000, 10000):
		for n in range(minN, maxN+10000, 10000):
			tileName = OSGB.grid_to_os_streetview_tile((e, n))
			print e, n, tileName
			tileCode = tileName[0].lower()
			fina = "out/"+str(tileCode[:2])+"/"+str(tileCode[:4])+"_OST50CONT_20130612.osm.bz2"
			if not os.path.exists(fina): continue
			fiList.append(fina)
			
	nextObjId = {"node": -1, "way": -1, "relation": -1}
	idMapping = {}

	for fina in fiList:
		MergeFile(fina, "node", nextObjId, idMapping, out)

	for fina in fiList:
		MergeFile(fina, "way", nextObjId, idMapping, out)

	for fina in fiList:
		MergeFile(fina, "relation", nextObjId, idMapping, out)

	out.write("</osm>\n")
	out.close()


