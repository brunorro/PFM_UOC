#!/usr/bin/python
from Exceptions import *
import os

try:
	import gtk,pygtk
	pygtk.require("2.0")
except:
	raise GTKLibraryNotFoundException()


class PreferencesDialog:

	def __init__ (self, configObject):
		self.configObject = configObject

		self.builder = gtk.Builder()
		self.builder.add_from_file("./resources/PreferencesDialog.glade")
		self.preferencesDialog = self.builder.get_object("PreferencesDialog")

		self.deviceNumberCombobox = self.builder.get_object("DeviceNumberCombobox")
		self.deviceNumberListStore = self.builder.get_object("DeviceNumberListStore")
		self.populateDeviceCombobox()

		self.accessDbCombobox = self.builder.get_object("AccessDbCombobox")

		self.accessDbComboListStore = self.builder.get_object("AccessDbComboListStore")
		self.accessDbTreeListStore =self.builder.get_object("AccessDbTreeListStore")

		self.biometricDbCombobox = self.builder.get_object("BiometricDbCombobox")

		self.biometricDbComboListStore = self.builder.get_object("BiometricDbComboListStore")
		self.biometricDbTreeListStore =self.builder.get_object("BiometricDbTreeListStore")

		self.setCameraDevice()
		self.populateAccessDbData()
		self.populateBiometricDbData()

		self.builder.connect_signals(self)

#cellrenderertext.connect('edited', edited_cb, (model, col_num))
#def edited_cb(cell, path, new_text, user_data):
#      liststore, column = user_data
#      liststore[path][column] = new_text
#      return

	def populateDeviceCombobox(self):
		self.deviceNumberListStore.clear()
		videoDeviceNameList= [ f for f in os.listdir('/dev/') if f.count("video")]

		for videoDeviceName in videoDeviceNameList:
			videoDeviceNumber = int(videoDeviceName.strip("video"))
			self.deviceNumberListStore.append(["/dev/"+videoDeviceName,int(videoDeviceNumber)])

	def setCameraDevice(self):
		print self.configObject.cameraDevice
		i = self.deviceNumberListStore.get_iter_first()
		while i!=None:
			if self.deviceNumberListStore.get_value(i,1)==int(self.configObject.cameraDevice):
				self.deviceNumberCombobox.set_active_iter(i)
			i=self.deviceNumberListStore.iter_next(i)

	def populateAccessDbData(self):
		for dbType in self.configObject.DB_TYPES.keys():
			self.accessDbComboListStore.append([self.configObject.DB_TYPES[dbType],dbType])

		i = self.accessDbComboListStore.get_iter_first()
		while i!=None:
			if self.accessDbComboListStore.get_value(i,1)==self.configObject.accessDbType:
				self.accessDbCombobox.set_active_iter(i)
			i=self.accessDbComboListStore.iter_next(i)

		for param in self.configObject.accessDbParams.keys():
			self.accessDbTreeListStore.append([param,self.configObject.accessDbParams[param]])


	def populateBiometricDbData(self):
		for dbType in self.configObject.DB_TYPES.keys():
			self.biometricDbComboListStore.append([self.configObject.DB_TYPES[dbType],dbType])

		i = self.biometricDbComboListStore.get_iter_first()
		while i!=None:
			if self.biometricDbComboListStore.get_value(i,1)==self.configObject.biometricDbType:
				self.biometricDbCombobox.set_active_iter(i)
			i=self.biometricDbComboListStore.iter_next(i)

		for param in self.configObject.biometricDbParams.keys():
			self.biometricDbTreeListStore.append([param, self.configObject.biometricDbParams[param]])

	def on_BiometricDbCombobox_changed (self, widget, data=None):
		self.biometricDbTreeListStore.clear()

		dbType = self.biometricDbComboListStore.get_value(self.biometricDbCombobox.get_active_iter(),1)
		if dbType == self.configObject.biometricDbType:
			for param in self.configObject.biometricDbParams.keys():
				self.biometricDbTreeListStore.append([param, self.configObject.biometricDbParams[param]])
		else:
			for param in self.configObject.DB_PARAMS[dbType]:
				self.biometricDbTreeListStore.append([param, ""])

	def on_AccessDbCombobox_changed (self, widget, data=None):
		self.accessDbTreeListStore.clear()
		dbType = self.accessDbComboListStore.get_value(self.accessDbCombobox.get_active_iter(),1)

		if dbType == self.configObject.accessDbType:
			for param in self.configObject.accessDbParams.keys():
				self.accessDbTreeListStore.append([param, self.configObject.accessDbParams[param]])

		else:
			for param in self.configObject.DB_PARAMS[dbType]:
				self.accessDbTreeListStore.append([param, ""])

	#	for param in self.configObject.accessDbParams.keys():
	#		self.accessDbTreeListStore.append([param,self.configObject.accessDbParams[param]])

	def on_PreferencesCancelButton_clicked(self, widget, data=None):
		print "Cancelados cambios"
		self.preferencesDialog.hide()

	def on_PreferencesApplyButton_clicked(self, widget, data=None):
		activeDevice = self.deviceNumberCombobox.get_active_iter()

		if (self.configObject.cameraDevice!=self.deviceNumberListStore.get_value(activeDevice, 1)):
			self.configObject.cameraDevice=self.deviceNumberListStore.get_value(activeDevice, 1)
		print ("Camara cambiada a %d " % self.configObject.cameraDevice )

	def on_PreferencesAcceptButton_clicked(self, widget, data=None):
		print "Guardando Cambios"

	def on_RefreshDevicesButton_clicked(self, widget, data=None):
		self.populateDeviceCombobox()
	

if __name__=="__main__":
	
	from Configuration import *

	config = Configuration("./resources/prueba.xml")
	config.readCameraConfiguration()
	config.readAccessDbConfiguration()
	config.readBiometricDbConfiguration()

	pd = PreferencesDialog(config)
	pd.setCameraDevice()
	pd.populateAccessDbData()
	pd.populateBiometricDbData()

	pd.preferencesDialog.run()

