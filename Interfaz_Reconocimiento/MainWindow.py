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

		self.builder = gtk.Builder()
		self.builder.add_from_file("./resources/MainWindow.glade")
		self.mainWindow = self.builder.get_object("MainWindow")
		self.mainImage = self.builder.get_object("MainDrawingarea")
		self.mainTextview = self.builder.get_object("MainTextview")
		self.mainTextbuffer = self.mainTextview.get_buffer()

		self.showFeaturesCheckmenuitem = self.builder.get_object("ShowFeaturesCheckmenuitem")
		self.showFacesCheckmenuitem = self.builder.get_object("ShowFacesCheckmenuitem")
		self.grayCheckmenuitem = self.builder.get_object("GrayCheckmenuitem")

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

#	def set_original_size(self, widget):
#		self.MainImage.window.resize(640,480)

	def on_MainDrawingarea_expose_event(self, widget, data):
		
		[img_width,img_height] = self.mainImage.window.get_size()
		if self.captureDevice!=None:
			faces = self.captureDevice.getFaces()

			if len(faces)>0:
				self.mainTextbuffer.insert_at_cursor("Individuo detectado\n")
				self.mainTextview.scroll_to_mark(self.mainTextbuffer.get_insert(),0.0)

			#if time.time()-self.initTime >= 30.0:
			#	self.mainTextbuffer.insert_at_cursor("Frames por segundo: %f \n" % (self.redrawCounter/30.0))
			#	self.mainTextview.scroll_to_mark(self.mainTextbuffer.get_insert(),0.0)
			#	self.redrawCounter = 0
			#	self.initTime=time.time()
			#else:
			#	self.redrawCounter+=1

        		self.mainImage.window.draw_pixbuf(None,(self.parentClass.captureDevice.getPixbuf()).scale_simple(img_width, img_height,gtk.gdk.INTERP_NEAREST),0,0,0,0)
			self.mainImage.queue_draw()
		else:
			self.mainTextbuffer.insert_at_cursor("Camara no configurada\n")
			self.mainTextview.scroll_to_mark(self.mainTextbuffer.get_insert(),0.0)

	def on_QuitImagemenuitem_activate(self,widget):
		self.parentClass.quit()

	def exceptionMessageDialog (self, title, msg):
		md= gtk.MessageDialog(self.mainWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)
		md.set_title(title)
		md.run()
		md.destroy()

	def on_ShowFeaturesCheckmenuitem_toggled(self, widget, data=None):
		if self.showFeaturesCheckmenuitem.get_active():
			print "Encuadrar rasgos activo"
			self.captureDevice.drawFeatures=1
		else:
			print "Encuadrar rasgos inactivo"
			self.captureDevice.drawFeatures=0


	def on_ShowFacesCheckmenuitem_toggled(self, widget, data=None):
		if self.showFacesCheckmenuitem.get_active():
			self.showFeaturesCheckmenuitem.set_inconsistent(False)
			self.showFeaturesCheckmenuitem.set_active(True)
			self.captureDevice.drawFaces=1
			print "Encuadrar caras activo"
		else:
			self.showFeaturesCheckmenuitem.set_inconsistent(True)
			self.captureDevice.drawFaces=0
			print "Encuadrar caras inactivo"


	def on_GrayCheckmenuitem_toggled(self, widget, data=None):
		if self.grayCheckmenuitem.get_active():
			self.captureDevice.gray=1
			print "Escala de grises activo"
		else:
			self.captureDevice.gray=0
			print "Escala de grises inactivo"

