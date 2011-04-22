#!/usr/bin/python
import xml.dom.minidom 

class Configuration:
	""" Almacenamiento de parametros de la aplicacion """

	def __init__(self, configFile):
		""" Constructora
			\param configFile Fichero XML del que leer la configuracion.

			Se encarga de inicializar la clase con los parametros obtenidos del XML. Caso que no existiesen, aplica parametros por defecto.
		"""

		self.DB_TYPES= {'SQLITE': 'Sqlite', 'POSTGRES': 'PostgreSQL'}
		self.DB_PARAMS= {'SQLITE': ["dbFile"], 'POSTGRES':["dbServer","dbName","dbPort","dbUser","dbPassword"]}
		self.CAMERA_PARAMS={'bright':'', 'hue':'', 'saturation':''}

		self.setDefaultAccessDbParams()
		self.setDefaultBiometricDbParams()
		self.setDefaultCameraParams()
		self.setDefaultRecoParams()

		try:
			self.xmlConfig = xml.dom.minidom.parse(configFile)
		except:
			print "Couldn't find configuration file. Setting default parameters"

		try:
			self.readCameraConfiguration()
		except: 
			print "Setting default camera settings"

		try: 
			self.readAccessDbConfiguration()
		except:
			print "Setting default access db settings"

		try:
			self.readBiometricDbConfiguration()
		except: 
			print "Setting default access db settings"

		try:
			self.readRecoPreferences()
		except: 
			print "Setting default Recognizer settings"


	def setDefaultAccessDbParams(self):
		self.accessDbType="SQLITE"
		self.accessDbParams = {}

	def setDefaultBiometricDbParams(self):
		self.biometricDbType="SQLITE"
		self.biometricDbParams = {}

	def setDefaultCameraParams(self):
		self.cameraDevice = int(1)
		self.cameraParams = {}

	def setDefaultRecoParams(self):
		self.recoPreferences = {}


	def readAccessDbConfiguration(self):
		""" Obtiene parametros de la base de datos de accesos """
		
	#try:
		dbElement = self.xmlConfig.getElementsByTagName("accessDatabase")

		if len(dbElement)>1:
			print "There is more than one XML database node. Using the first one"

		for dbConfigNode in dbElement[0].childNodes:

			nodeName = str(dbConfigNode.localName)

			if nodeName == "dbDriver":
				self.accessDbType=(dbConfigNode.childNodes[0].data).strip()

				for par in self.DB_PARAMS[self.accessDbType]:
					self.accessDbParams[par]= ''

			if nodeName == "param":
				attribNumber = dbConfigNode.attributes.length
				for i in range (0,attribNumber):
					if dbConfigNode.attributes.item(i).localName=="name":

						if dbConfigNode.childNodes[0].nodeType == dbConfigNode.childNodes[0].TEXT_NODE:
							self.accessDbParams[str(dbConfigNode.attributes.item(i).value).strip()]=str(dbConfigNode.childNodes[0].data).strip()

			
		#except:
		#	print "Database section doesn't exist in the XML config file"

	def readBiometricDbConfiguration(self):
		""" Obtiene parametros de la base de datos de rasgos biometricos """

		#try:
		dbElement = self.xmlConfig.getElementsByTagName("biometricDatabase")

		if len(dbElement)>1:
			print "There is more than one XML database node. Using the first one"

		for dbConfigNode in dbElement[0].childNodes:

			nodeName = str(dbConfigNode.localName)
			if nodeName == "dbDriver":
				self.biometricDbType=(dbConfigNode.childNodes[0].data).strip()
				for par in self.DB_PARAMS[self.biometricDbType]:
					self.biometricDbParams[par]= ''

			if nodeName == "param":
				attribNumber = dbConfigNode.attributes.length
				for i in range (0,attribNumber):
					if dbConfigNode.attributes.item(i).localName=="name":
					#self.dbParams.append(str(dbConfigNode.attributes.item(i).value))

						if dbConfigNode.childNodes[0].nodeType == dbConfigNode.childNodes[0].TEXT_NODE:
							self.biometricDbParams[str(dbConfigNode.attributes.item(i).value).strip()]=str(dbConfigNode.childNodes[0].data).strip()

		#except:
		#	print "Database section doesn't exist in the XML config file"

	def readCameraConfiguration(self):
		""" Lee los parametros de configuracion de la camara """
	
		cameraElement = self.xmlConfig.getElementsByTagName("camera")

		if len(cameraElement)>1:
			print "More than one entry for the camera. Using the first one"
	
		for cameraConfigNode in cameraElement[0].childNodes:
			nodeName = str(cameraConfigNode.localName)
			if nodeName == "deviceNumber":
				self.cameraDevice=int((cameraConfigNode.childNodes[0].data).strip())

			if nodeName == "cascadeFile":
				self.cascadeFile=str((cameraConfigNode.childNodes[0].data).strip())

			if nodeName == "param":
				attribNumber = cameraConfigNode.attributes.length
				for i in range (0,attribNumber):
					if cameraConfigNode.attributes.item(i).localName=="name":
						if cameraConfigNode.childNodes[0].nodeType == cameraConfigNode.childNodes[0].TEXT_NODE:
							self.cameraParams[str(cameraConfigNode.attributes.item(i).value).strip()]=str(cameraConfigNode.childNodes[0].data).strip()

	def readRecoPreferences(self):
		""" Lee las preferencias de la aplicacion de reconocimiento """
		recoElement = self.xmlConfig.getElementsByTagName("recoPreferences")

		if len(recoElement)>1:
			print "More than one entry for the camera. Using the first one"
	
		for recoConfigNode in recoElement[0].childNodes:
			nodeName = str(recoConfigNode.localName)

			if nodeName == "Gray":
				self.recoPreferences['Gray']=int((recoConfigNode.childNodes[0].data).strip())
			if nodeName == "ShowFaces":
				self.recoPreferences['ShowFaces']=int((recoConfigNode.childNodes[0].data).strip())
			if nodeName == "ShowFeatures":
				self.recoPreferences['ShowFeatures']=int((recoConfigNode.childNodes[0].data).strip())

#			if nodeName == "param":
#				attribNumber = cameraConfigNode.attributes.length
#				for i in range (0,attribNumber):
#					if cameraConfigNode.attributes.item(i).localName=="name":
#						if cameraConfigNode.childNodes[0].nodeType == cameraConfigNode.childNodes[0].TEXT_NODE:
#							self.cameraParams[str(cameraConfigNode.attributes.item(i).value).strip()]=str(cameraConfigNode.childNodes[0].data).strip()
	

	def saveConfigXML(self, fileName):
		""" Guarda un fichero xml con la configuracion actual 

			\param fileName El fichero en el que se escribira la configuracion
		"""
		try:
			f = open(fileName, "w")
			f.write(self.xmlConfig.toprettyxml("", "", "UTF-8"))
		finally:
			f.close()


if __name__=="__main__":
	config = Configuration("./resources/prueba.xml")

	print config.cameraDevice
	print config.cameraParams
	print config.cascadeFile
	kk=[]
	for par in config.cameraParams.keys():
		kk.append([par, config.cameraParams[par]])
	print kk

	print config.accessDbType
	print config.accessDbParams
	kk=[]
	for par in config.accessDbParams.keys():
		kk.append([par, config.accessDbParams[par]])
	print kk
		
	print config.biometricDbType
	print config.biometricDbParams
	kk=[]
	for par in config.biometricDbParams.keys():
		kk.append([par, config.biometricDbParams[par]])
	print kk

	kk=[]
	for par in config.recoPreferences.keys():
		kk.append([par, config.recoPreferences[par]])
	print kk

	config.saveConfigXML("prueba.xml")
