#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
from xml.sax.saxutils import escape, quoteattr

class OsmOutput(object):
	def __init__(self, fina):

		self.fi = codecs.open(fina, "w", "utf-8")
		self.fi.write(u"<?xml version='1.0' encoding='UTF-8'?>\n")
		self.fi.write(u"<osm version='0.6' generator='writeosm.py'>\n")

	def __del__(self):
		self.fi.write(u"</osm>\n")
		self.fi.close()

	def WriteNode(self, objId, lat, lon, tags):
		self.fi.write(u"<node id='{0}' lat='{1}' lon='{2}'".format(int(objId), float(lat), float(lon)))
		if len(tags) == 0:
			self.fi.write(u" />\n")
		else:
			self.fi.write(u">\n")
			for key in tags:
				self.fi.write(u' <tag k={0} v={1} />\n'.format(quoteattr(escape(key)), quoteattr(escape(tags[key]))))
			self.fi.write(u"</node>\n")

	def WriteWay(self, wayId, nodeIds, tags):
		self.fi.write(u"<way id='{0}'>\n".format(int(wayId)))
		for nid in nodeIds:
			self.fi.write(u" <nd ref='{0}' />\n".format(int(nid)))
		for key in tags:
			self.fi.write(u' <tag k={0} v={1} />\n'.format(quoteattr(escape(key)), quoteattr(escape(tags[key]))))
		self.fi.write(u"</way>\n")



if __name__ == "__main__":
	
	osmOutput = OsmOutput("test.osm")
	osmOutput.WriteNode(-1, 51., -1., {'test':"\"'", 'test2':u"This has ♭"})
	osmOutput.WriteNode(-2, 50., -2., {})
	osmOutput.WriteWay(-1, [-1, -2], {"test3": "stuff"})

