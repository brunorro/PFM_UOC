#!/usr/bin/python
import xml.dom.minidom 

class Configuration:

	def __init__(self, configFile):
		try:
			self.xmlConfig = xml.dom.minidom.parse(configFile)
		except:
			print "Couldn't find configuration file. Setting default parameters"
			

#	def getDbConfiguration(self):
#		#try:
#			dbElement = self.xmlConfig.getElementsByTagName("database")
#
#			if len(dbElement)>1:
#				print "There is more than one XML database node. Using the first one"
#
#			for dbConfigNode in dbElement[0].childNodes:
#
#				nodeName = str(dbConfigNode.localName)
#				print nodeName
#
#				attribNumber = dbConfigNode.attributes.length
#
#				for i in range (0,attribNumber):
#					print "\tATRIBUTO: "+str(dbConfigNode.attributes.item(i).localName) +" -> "+str(dbConfigNode.attributes.item(i).value)
#
#				for dbOption in dbConfigNode.childNodes:
#
#					if dbOption.nodeType == dbOption.TEXT_NODE:
#						print "\tVALOR -> "+str(dbOption.data)
#
#			
#		#except:
#		#	print "Database section doesn't exist in the XML config file"

		
	def getDbConfiguration(self):
			self.dbType="SQLITE"
			self.dbParams = []

		#try:
			dbElement = self.xmlConfig.getElementsByTagName("database")

			if len(dbElement)>1:
				print "There is more than one XML database node. Using the first one"

			for dbConfigNode in dbElement[0].childNodes:

				nodeName = str(dbConfigNode.localName)
				if nodeName == "dbDriver":
					self.dbType=dbConfigNode.childNodes[0].data

				if nodeName == "param":
					attribNumber = dbConfigNode.attributes.length
					for i in range (0,attribNumber):
						if dbConfigNode.attributes.item(i).localName=="name":
						#self.dbParams.append(str(dbConfigNode.attributes.item(i).value))

							if dbConfigNode.childNodes[0].nodeType == dbConfigNode.childNodes[0].TEXT_NODE:
								self.dbParams.append([str(dbConfigNode.attributes.item(i).value),str(dbConfigNode.childNodes[0].data)])
			
		#except:
		#	print "Database section doesn't exist in the XML config file"

def print_node_info(node, indents):
	indentstring=""
	for i in range(0,indents):
		indentstring+="\t"

	print indentstring+str(node.nodeName)
	if node.nodeType == node.TEXT_NODE:
		print indentstring + str(node.data)
	if node.attributes:
		print indentstring + "Tiene Atributos"
		for i in range(0, node.attributes.length):
			print indentstring + "-" + node.attributes.item(i).localName
			print indentstring + "-" + node.attributes.item(i).value
		
	#	print node.nodeValue
	#print indentstring+str(node.attributes)

	if node.hasChildNodes():
		for auxNode in node.childNodes:
			print_node_info(auxNode, indents+1)

if __name__=="__main__":
	config = Configuration("prueba.xml")
	config.getDbConfiguration()
#	for auxNode in config.xmlConfig.childNodes:
#		print_node_info(auxNode,0)

