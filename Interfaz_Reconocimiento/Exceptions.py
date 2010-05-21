#!/usr/bin/python

class GTKLibraryNotFoundException(Exception):
	def __init__(self):
		return

	def __str__(self):
		return "Libreria GTK no encontrada"

class OpenCVLibraryNotFoundException(Exception):
	def __init__(self):
		return

	def __str__(self):
		return "Libreria OpenCV no encontrada"

class CaptureDeviceParametersException(Exception):

	def __init__(self, errorList=[]):
		self.errorList = errorList
		return

	def appendError(str):
		self.errorList.append(str)

	def __str__(self):
		errorString = ""
		for str in self.errorList:
			errorString+=str+"\n"
		return errorString
