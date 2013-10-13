
import zipfile, os, cart, math
import xml.etree.ElementTree as ET
from ostn02python import OSTN02, OSGB
from shapely.geometry import LineString, Point

class ReadGml(object):

	def ReadGeometry(self, geo):
		for ch in geo:
			if ch.tag == "{http://www.opengis.net/gml/3.2}LineString":
				posListEl = ch.find('{http://www.opengis.net/gml/3.2}posList')
				posFloats = map(float, posListEl.text.split(" "))
				est = posFloats[0::2] 
				nth = posFloats[1::2]
				pts = []
				for e, n in zip(est, nth):
					(x,y,h) = OSTN02.OSGB36_to_ETRS89 (e, n)
					(gla, glo) = OSGB.grid_to_ll(x, y)
					#print e, n, gla, glo, h
					p = cart.LatLonToCart(math.radians(gla), math.radians(glo), 0.)
					pts.append(p)
				
				shp = LineString(pts)
				return shp

			if ch.tag == "{http://www.opengis.net/gml/3.2}Point":
				posEl = ch.find("{http://www.opengis.net/gml/3.2}pos")
				posFloat = map(float, posEl.text.split(" "))
				(x,y,h) = OSTN02.OSGB36_to_ETRS89 (posFloat[0], posFloat[1])
				(gla, glo) = OSGB.grid_to_ll(x, y)
				
				shp = Point(cart.LatLonToCart(math.radians(gla), math.radians(glo), 0.))
				#print shp
				return shp
			#print ch.tag

		return None

	def ReadSpotHeight(self, el):

		geoEl = el.find("{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}geometry")
		shp = self.ReadGeometry(geoEl)

		propEl = el.find("{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}propertyValue")
		return (shp, {'ele':propEl.text})

	def ReadContour(self, el):

		geoEl = el.find("{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}geometry")
		shp = self.ReadGeometry(geoEl)

		propEl = el.find("{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}propertyValue")
		return (shp, {'ele':propEl.text})

	def ReadMember(self, el):
		for ch in el:
			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}ContourLine":
				shp, tags = self.ReadContour(ch)
				return [shp, tags]

			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}SpotHeight":
				shp, tags = self.ReadSpotHeight(ch)
				return [shp, tags]

			print ch.tag
		return None

	def Read(self, gmlFi):
		root = ET.fromstring(gmlFi.read())
		data = []

		for ch in root:
		
			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}member":
				mem = self.ReadMember(ch)
				data.append(mem)
			else:
				print "Unprocessed tag:", ch.tag

		return data

def ReadGmlZip(archName):
	zipContent = zipfile.ZipFile(archName)
	fiList = zipContent.namelist()
	out = []

	for fina in fiList:
		extspl = os.path.splitext(fina)
		if extspl[1] == ".gml":
			print "Reading", fina
			readGml = ReadGml()
			memData = readGml.Read(zipContent.open(fina))
			print "Number of members:", len(memData)
			out.append(memData)

	return out

if __name__ == "__main__":
	archName = "/home/tim/Downloads/terr50_cgml_gb/data/so/so00_OST50CONT_20130612.zip"

	ReadGmlZip(archName)



