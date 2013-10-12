
import zipfile, os
import xml.etree.ElementTree as ET

class ReadGml(object):

	def ReadGeometry(self, geo):
		for ch in geo:
			print ch.tag
		#pass
		

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

