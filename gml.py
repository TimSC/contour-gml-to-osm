
import zipfile, os
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
				lonLat = []
				for e, n in zip(est, nth):
					(x,y,h) = OSTN02.OSGB36_to_ETRS89 (e, n)
					(gla, glo) = OSGB.grid_to_ll(x, y)
					#print e, n, gla, glo, h
					lonLat.append((glo, gla))
				
				shp = LineString(lonLat)
				#print shp

			if ch.tag == "{http://www.opengis.net/gml/3.2}Point":
				posEl = ch.find("{http://www.opengis.net/gml/3.2}pos")
				posFloat = map(float, posEl.text.split(" "))
				(x,y,h) = OSTN02.OSGB36_to_ETRS89 (posFloat[0], posFloat[1])
				(gla, glo) = OSGB.grid_to_ll(x, y)
				
				shp = Point(glo, gla)
				#print shp
			#print ch.tag
		

	def ReadSpotHeight(self, el):
		for ch in el:
			
			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}geometry":
				self.ReadGeometry(ch)
				continue

			#print ch.tag
		pass

	def ReadContour(self, el):
		for ch in el:
			
			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}geometry":
				self.ReadGeometry(ch)
				continue

			#print ch.tag

	def ReadMember(self, el):
		for ch in el:
			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}ContourLine":
				self.ReadContour(ch)
				continue

			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}SpotHeight":
				self.ReadSpotHeight(ch)
				continue

			print ch.tag

	def Read(self, gmlFi):
		root = ET.fromstring(gmlFi.read())
		for ch in root:
		
			if ch.tag == "{http://namespaces.ordnancesurvey.co.uk/elevation/contours/v1.0}member":
				self.ReadMember(ch)
			else:
				print ch.tag

if __name__ == "__main__":
	archName = "/home/tim/Downloads/terr50_cgml_gb/data/so/so00_OST50CONT_20130612.zip"

	zipContent = zipfile.ZipFile(archName)
	fiList = zipContent.namelist()

	for fina in fiList:
		extspl = os.path.splitext(fina)
		if extspl[1] == ".gml":
			readGml = ReadGml()
			readGml.Read(zipContent.open(fina))

