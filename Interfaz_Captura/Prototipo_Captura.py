#!/usr/bin/python

from Exceptions import *
from CaptureDevice import *
from MainWindow import *
from PreferencesDialog import *
from Configuration import *
from FaceSignature import *

class Capturador:
	
	def __init__(self):

		self.config = Configuration("./resources/prueba.xml")
		self.prefDialog = PreferencesDialog(self.config)

		self.faceSign = FaceSignature()

		self.captureDevice= CaptureDevice(self)
		self.MW = MainWindow(self)

		self.setCaptureDevice()

		self.MW.mainWindow.show()

		gtk.main()

	def openPreferencesDialog(self, tab=0):
		cameraAux = self.config.cameraDevice

		self.prefDialog.preferencesDialog.run()
		self.prefDialog.preferencesDialog.hide()

		if self.config.cameraDevice!=cameraAux:
			self.setCaptureDevice()

	def setCaptureDevice(self):
		try :
			self.captureDevice.setCaptureParameters(self.config.cameraDevice, self.config.cascadeFile)

		except CaptureDeviceParametersException ,e:
			self.MW.exceptionMessageDialog("Errores en dispositivo de captura", e.__str__())
			self.openPreferencesDialog(0)

	def quit(self, widget=None):
		gtk.main_quit()

if __name__=="__main__":
	c  = Capturador()
