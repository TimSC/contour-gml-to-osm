import bz2, os
import xml.etree.ElementTree as ET
from ostn02python import OSGB, OSTN02

def MergeFile(fina, ty, existing, fiOut):
	fi = bz2.BZ2File(fina)
	root = ET.fromstring(fi.read())

	for el in root:
		if el.tag != ty: continue
		objId = int(el.attrib['id'])
		if objId in existing: 
			print "skipping", el.tag, objId
			continue
		print el.tag, objId
		existing.add(objId)

		xml = ET.tostring(el, encoding="utf-8")
		fiOut.write(xml)

if __name__=="__main__":
	
	out = bz2.BZ2File("merge.osm.bz2","w")
	#out = open("merge.osm","wt")
	out.write("<?xml version='1.0' encoding='UTF-8'?>\n")
	out.write("<osm version='0.6' upload='true' generator='py'>\n")

	lats, lons = [51.383075,50.705752], [-1.955713,-0.729294]
	collectEastings = []
	collectNorthings = []

	#Convert to OS grid
	for lat in lats:
		for lon in lons:
			
			(x2,y2) = OSGB.ll_to_grid(lat, lon)
			e, n, h = OSTN02.ETRS89_to_OSGB36(x2,y2,0.)
	
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


	for e in range(minE, maxE+10000, 10000):
		for n in range(minN, maxN+10000, 10000):
			print e, n, OSGB.grid_to_os_streetview_tile((e, n))

	exit(0)
	
	fiList = []
	for x in range(xtile1, xtile2+1):
		for y in range(ytile2, ytile1+1):
			rootPath = "existing/12"
			dirName = rootPath+"/"+str(x)
			fina = dirName+"/"+str(y)+".osm.bz2"
			if os.path.isfile(fina):
				fiList.append(fina)

	for fina in fiList:
		MergeFile(fina, "node", existing, out)

	for fina in fiList:
		MergeFile(fina, "way", existing, out)

	for fina in fiList:
		MergeFile(fina, "relation", existing, out)

	out.write("</osm>\n")
	out.close()


