import gml, writeosm, pickle, bz2

if __name__ == "__main__":
	
	archName = "/media/data/home/tim/kinatomicw/Downloads/terr50/data/so/so00_OST50CONT_20130612.zip"
	if 1:
		gmlData = gml.ReadGmlZip(archName)
		pickle.dump(gmlData, open("gmlData.dat", "wb"), protocol = -1) 
	else:
		gmlData = pickle.load(open("gmlData.dat", "rb"))
	
	print "GML files in archive", len(gmlData)
	


	for gmlDataFi in gmlData:
		print "Simplify"
		for objData in gmlDataFi:
			shp, tags = objData
			objData[0] = shp.simplify(10.)

		print "Write output"
		writeosm.ShapelyToOsm(gmlDataFi, bz2.BZ2File("test.osm.bz2","w"))

