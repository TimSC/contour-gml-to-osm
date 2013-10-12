import gml, writeosm

if __name__ == "__main__":
	
	archName = "/home/tim/Downloads/terr50_cgml_gb/data/so/so00_OST50CONT_20130612.zip"
	gmlData = gml.ReadGmlZip(archName)
	
	print "GML files in archive", len(gmlData)

	
