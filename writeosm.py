#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.saxutils import escape, quoteattr

class OsmOutput(object):
	def __init__(self, fina):

		if hasattr(fina, 'write'):
			self.fi = fina
		else:
			self.fi = open(fina, "wt")

		self.fi.write(u"<?xml version='1.0' encoding='UTF-8'?>\n".encode('UTF-8'))
		self.fi.write(u"<osm version='0.6' generator='writeosm.py'>\n".encode('UTF-8'))

	def __del__(self):
		self.fi.write(u"</osm>\n".encode('UTF-8'))
		self.fi.close()

	def WriteNode(self, objId, lat, lon, tags):
		self.fi.write(u"<node id='{0}' lat='{1}' lon='{2}'".format(int(objId), float(lat), float(lon)).encode('UTF-8'))
		if len(tags) == 0:
			self.fi.write(u" />\n".encode('UTF-8'))
		else:
			self.fi.write(u">\n".encode('UTF-8'))
			for key in tags:
				self.fi.write(u' <tag k={0} v={1} />\n'.format(quoteattr(escape(key)), quoteattr(escape(tags[key]))).encode('UTF-8'))
			self.fi.write(u"</node>\n".encode('UTF-8'))

	def WriteWay(self, wayId, nodeIds, tags):
		self.fi.write(u"<way id='{0}'>\n".format(int(wayId)).encode('UTF-8'))
		for nid in nodeIds:
			self.fi.write(u" <nd ref='{0}' />\n".format(int(nid)).encode('UTF-8'))
		for key in tags:
			self.fi.write(u' <tag k={0} v={1} />\n'.format(quoteattr(escape(key)), quoteattr(escape(tags[key]))).encode('UTF-8'))
		self.fi.write(u"</way>\n".encode('UTF-8'))

	def WriteRelation(self, wayId, members, tags):
		self.fi.write(u"<relation id='{0}'>\n".format(int(wayId)).encode('UTF-8'))
		for member in members:
			self.fi.write(u" <member type={0} ref='{1}' role={2}/>\n".format(
				quoteattr(escape(member[0])), 
				int(member[1]), 
				quoteattr(escape(member[2]))
				).encode('UTF-8'))
		for key in tags:
			self.fi.write(u' <tag k={0} v={1} />\n'.format(quoteattr(escape(key)), quoteattr(escape(tags[key]))).encode('UTF-8'))
		self.fi.write(u"</relation>\n".encode('UTF-8'))

if __name__ == "__main__":
	
	osmOutput = OsmOutput("test.osm")
	osmOutput.WriteNode(-1, 51., -1., {'test':"\"'", 'test2':u"This has ♭"})
	osmOutput.WriteNode(-2, 50., -2., {})
	osmOutput.WriteWay(-1, [-1, -2], {"test3": "stuff"})


	osmOutput.WriteRelation(-1, [("node", -1, "weird"), ], {"foo":"bar"})


