import gml, writeosm, pickle, bz2, os

if __name__ == "__main__":
	
	if not os.path.exists("out"):
		os.mkdir("out")

	startFolder = "/media/data/home/tim/kinatomicw/Downloads/terr50/data"
	for gridref in os.listdir(startFolder):
		gridFolder = startFolder + "/" + gridref

		if not os.path.exists("out/"+gridref):
			os.mkdir("out/"+gridref)

		for fina in os.listdir(gridFolder):
			finasp = os.path.splitext(fina)
			print fina

			gmlData = gml.ReadGmlZip(gridFolder+"/"+fina)
			for gmlDataFi in gmlData:
				print "Simplify"
				simplifiedObjs = []

				for objData in gmlDataFi:
					if objData is None: continue
					shp, tags = objData
					objData[0] = shp.simplify(10.)
					simplifiedObjs.append(objData)

				print "Write output"
				writeosm.ShapelyToOsm(simplifiedObjs, bz2.BZ2File("out/"+gridref+"/"+finasp[0]+".osm.bz2","w"))



