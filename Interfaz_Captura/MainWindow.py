#!/usr/bin/python
import sys, time

from Exceptions import *
from CaptureDevice import *

try:
	from opencv import cv,highgui
except:
	raise OpenCVLibraryNotFoundException()

try:
	import gtk,pygtk
	pygtk.require("2.0")
except:
	raise GTKLibraryNotFoundException()


class MainWindow():

	def __init__ (self, parentClass):
		self.parentClass = parentClass
		self.captureDevice = self.parentClass.captureDevice
		self.faceSign = self.parentClass.faceSign

		self.builder = gtk.Builder()
		self.builder.add_from_file("./resources/MainWindow.glade")
		self.mainWindow = self.builder.get_object("MainWindow")
		self.mainImage = self.builder.get_object("MainDrawingarea")
		self.mainStatusbar = self.builder.get_object("MainStatusbar")

		self.showFeaturesCheckmenuitem = self.builder.get_object("ShowFeaturesCheckmenuitem")
		self.showFacesCheckmenuitem = self.builder.get_object("ShowFacesCheckmenuitem")
		self.grayCheckmenuitem = self.builder.get_object("GrayCheckmenuitem")

		self.idEntry = self.builder.get_object("IdEntry")

		self.pb = gtk.gdk.pixbuf_new_from_file("./resources/NoSignature.png")
		self.featuresDrawingarea = self.builder.get_object("FeaturesDrawingarea")

		self.showFeaturesCheckmenuitem.set_active(self.parentClass.config.recoPreferences['ShowFeatures'])
		self.showFacesCheckmenuitem.set_active(self.parentClass.config.recoPreferences['ShowFaces'])
		self.grayCheckmenuitem.set_active(self.parentClass.config.recoPreferences['Gray'])

		if self.mainWindow:
			self.mainWindow.connect("destroy", self.parentClass.quit)

		self.builder.connect_signals(self)
		#self.redrawCounter = 0
		#self.initTime = time.time()
		#self.salto=0

	def on_PreferencesImagemenuitem_activate(self,widget):
		self.parentClass.openPreferencesDialog()

	def on_MainDrawingarea_expose_event(self, widget, data):
		
		[img_width,img_height] = self.mainImage.window.get_size()
		[sign_width, sign_height] = self.featuresDrawingarea.window.get_size()

		if self.captureDevice!=None:
			faces = self.captureDevice.getFaces()

			if len(faces)>0:
				self.mainStatusbar.push(0,"Individuo detectado")
				self.faceSign.setFromImage(self.captureDevice.getScaledFaceImage())
				self.featuresDrawingarea.window.draw_pixbuf(None, (self.faceSign.getPixbufSignature()).scale_simple(img_width, sign_height, gtk.gdk.INTERP_BILINEAR),0,0,0,0)
				print self.faceSign.getBitSignature()
				
			else:
				self.featuresDrawingarea.window.draw_pixbuf(None, self.pb.scale_simple(img_width, sign_height, gtk.gdk.INTERP_BILINEAR),0,0,0,0)
				self.mainStatusbar.push(0,"")

        		self.mainImage.window.draw_pixbuf(None,(self.parentClass.captureDevice.getPixbuf()).scale_simple(img_width, img_height,gtk.gdk.INTERP_NEAREST),0,0,0,0)
			self.mainImage.queue_draw()
		else:
			self.mainStatusbar.push(0, "Camara no configurada")

	def on_QuitImagemenuitem_activate(self,widget):
		self.parentClass.quit()

	def exceptionMessageDialog (self, title, msg):
		md= gtk.MessageDialog(self.mainWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)
		md.set_title(title)
		md.run()
		md.destroy()

	def on_ShowFeaturesCheckmenuitem_toggled(self, widget, data=None):
		if self.showFeaturesCheckmenuitem.get_active():
			self.mainStatusbar.push(0, "Encuadrar rasgos activado")
			self.captureDevice.drawFeatures=1
		else:
			self.mainStatusbar.push(0, "Encuadrar rasgos desactivado")
			self.captureDevice.drawFeatures=0


	def on_ShowFacesCheckmenuitem_toggled(self, widget, data=None):
		if self.showFacesCheckmenuitem.get_active():
			self.showFeaturesCheckmenuitem.set_inconsistent(False)
			self.showFeaturesCheckmenuitem.set_active(True)
			self.captureDevice.drawFaces=1
			self.mainStatusbar.push(0, "Encuadrar caras activado")

		else:
			self.showFeaturesCheckmenuitem.set_inconsistent(True)
			self.captureDevice.drawFaces=0
			self.mainStatusbar.push(0, "Encuadrar caras desactivado")

	def on_GrayCheckmenuitem_toggled(self, widget, data=None):
		if self.grayCheckmenuitem.get_active():
			self.captureDevice.gray=1
			self.mainStatusbar.push(0, "Imagen en escala de grises")
		else:
			self.captureDevice.gray=0
			self.mainStatusbar.push(0, "Imagen en color")

	def on_SaveButton_clicked(self, widget, data=None):
		print "Click"
		id = self.idEntry.get_text()
		if id=="":
			print "No hay identificador de individuo !!"
		else:
			#imgName = "/home/bruno/pfc_UOC/PFM_UOC/Interfaz_GestorAcccesos/resources/imgEmployees/"+id+".jpg"
			#cvSaveImage(imgName, self.captureDevice.getScaledFaceImage())
			print self.faceSign.getBitSignature()

