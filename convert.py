import gml, writeosm, pickle

if __name__ == "__main__":
	
	archName = "/home/tim/Downloads/terr50_cgml_gb/data/so/so00_OST50CONT_20130612.zip"
	if 1:
		gmlData = gml.ReadGmlZip(archName)
		pickle.dump(gmlData, open("gmlData.dat", "wb"), protocol = -1) 
	else:
		gmlData = pickle.load(open("gmlData.dat", "rb"))
	
	print "GML files in archive", len(gmlData)
	


	for gmlDataFi in gmlData:
		print "Simplify"
		for objData in shapelyData:
			shp, tags = objData
			objData[0] = shp.simplify(10.)

		print "Write output"
		writeosm.ShapelyToOsm(gmlDataFi, "test.osm")

