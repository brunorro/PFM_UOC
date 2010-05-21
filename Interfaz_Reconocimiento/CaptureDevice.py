#!/usr/bin/python
""" @package InterfazReconocimiento """

from Exceptions import *
import time

try:
	from opencv.cv import *
	from opencv.highgui import *
except:
	raise OpenCVLibraryNotFoundException()

try :
	import gtk,pygtk
	pygtk.require("2.0")
except:
	raise GTKLibraryNotFoundException()

""" Control del dispositivo de captura

Esta clase realiza todas las operaciones sobre el dispositivo de captura empleado por la aplicacion. Entre otras se encarga de 
extraer las caracteristicas de cada individuo, de interrogar al dispositivo para la obtencion de frames, de controlar el tipo 
de frames obtenidos, etc. """

class CaptureDevice:
	""" Control del dispositivo de captura

	Esta clase realiza todas las operaciones sobre el dispositivo de captura empleado por la aplicacion. Entre otras se encarga de 
	extraer las caracteristicas de cada individuo, de interrogar al dispositivo para la obtencion de frames, de controlar el tipo 
	de frames obtenidos, etc. 
	\param camera Entero identificador de la camara
	\param cascade Fichero de identificador en cascada de caras
	\param image Imagen auxiliar en memoria de lo capturado por la camara
	\param grayframe Imagen anterior convertida a escala de grises
	\param frameWidth Anchura de los frames anteriores
	\param frameHeight Altura de los frames anteriores
	\param gray Mostrar imagen en escala de grises
	\param drawFacebox Recuadrar las caras encontradas
	\param drawFeatures Recuadrar los rasgos encontrados
	"""

	camera = None
	cascade = None

	image = None
	grayframe = None
	frameWidth = 0
	frameHeight = 0

	faceLocations = []

	gray=0
	drawFacebox = 1
	drawFeatures = 1

	def __init__(self, parentClass):
		""" Constructora de la clase
		\param parentClass Clase desde la que es invocada
		\param cascadeClassifierFile Fichero de clasificador en cascada
		\param captureDeviceNumber Numero de dispositivo de video a emplear

		La constructora hace lo siguiente:
		\li Inicializa el clasificador en cascada para la deteccion de caracteristicas faciales
		\li Crea un dispositivo de video para capturar datos desde el 
		\li Inicializa variables auxiliares de la clase"""
		#self.camera = None 
		#self.image = None
		#self.grayframe = None
		
		#self.faceLocationList =[]

		#self.gray = 0
		#self.drawFacebox = 1
		#self.drawFeatures = 1


	def setCaptureParameters(self, captureDeviceNumber, cascadeClassifierFile):

		configExceptionArray = []

		self.cascade = cvLoadHaarClassifierCascade(cascadeClassifierFile, cvSize(1,1))

		if self.cascade==None:
			configExceptionArray.append("No se encontro el fichero %s. ERROR GRAVE."% (cascadeClassifierFile))

		if self.camera != None:
			cvReleaseCapture(self.camera)
			self.camera=None

		self.camera = cvCreateCameraCapture(captureDeviceNumber)

		if self.camera==None:
			configExceptionArray.append("No se encontro el dispositivo de captura numero %d. Configurar dispositivo de captura de manera correcta" %(captureDeviceNumber))

			self.image = cvLoadImage("resources/NoImage.jpg")
			self.frameWidth = 640
			self.frameHeight= 400
			return []

		if len(configExceptionArray)>0:
			e = CaptureDeviceParametersException(configExceptionArray)
			raise e
		else:
			print "Configuracion correcta. Creando estructuras de datos para las imagenes"

			#highgui.cvSetCaptureProperty(self.camera, highgui.CV_CAP_PROP_FRAME_WIDTH, 320.0)
			self.frameWidth = int( cvGetCaptureProperty(self.camera, CV_CAP_PROP_FRAME_WIDTH) )
			#highgui.cvSetCaptureProperty(self.camera, highgui.CV_CAP_PROP_FRAME_HEIGHT, 240.0)
			self.frameHeight = int( cvGetCaptureProperty(self.camera, CV_CAP_PROP_FRAME_HEIGHT) )

			print "llego a conseguir el ancho y alto"
			#self.image=None
			#self.grayframe=None

			self.image= cvCreateImage(cvSize(self.frameWidth,self.frameHeight),8,3)
			self.grayframe = cvCreateImage(cvGetSize(self.image),8,1)
			print "Recreo imagenes"

		#cv.CV_CAP_PROP_POS_MSEC #cv.CV_CAP_PROP_POS_FRAMES #cv.CV_CAP_PROP_POS_AVI_RATIO
		#cv.CV_CAP_PROP_FRAME_WIDTH #cv.CV_CAP_PROP_FRAME_HEIGHT #cv.CV_CAP_PROP_FPS
		#cv.CV_CAP_PROP_FOURCC #cv.CV_CAP_PROP_FRAME_COUNT #cv.CV_CAP_PROP_BRIGHTNESS
		#cv.CV_CAP_PROP_CONTRAST #cv.CV_CAP_PROP_SATURATION #cv.CV_CAP_PROP_HUE


	def getFaceLocations(self):
		""" Obtiene la localizacion de las caras 
		A partir del ultimo fotograma obtenido, este metodo obtiene la ubicacion de las caras."""

		self.faceLocationList =[]

		if self.camera==None:
			self.image = cvLoadImage("resources/NoImage.jpg")
			self.frameWidth = 640
			self.frameHeight= 400
			return []

		else:	
			self.image = cvQueryFrame(self.camera)
			cvFlip(self.image, self.image, 1)

			cvCvtColor(self.image,self.grayframe,CV_BGR2GRAY)

       			# create storage
			storage = cvCreateMemStorage(0)
			cvClearMemStorage(storage)

			#cv.cvEqualizeHist(self.image, self.grayframe)
       			# detect objects

			faces = cvHaarDetectObjects(self.image, self.cascade, storage, 1.2, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(50, 50))

			for i in faces:
				self.faceLocationList.append([int(i.x), int(i.y), int(i.x)+int(i.width), int(i.y)+int(i.height), int(i.width), int(i.height)])

	def getPixbuf(self):
		""" Genera un gtk-pixbuf
		
		Este metodo devuelve un pixbuf para mostrarlo en una aplicacion GTK a partir del ultimo frame obtenido via opencv. """

		rectanglePointList = []

		if self.drawFacebox:
			for face in self.faceLocationList:
				initPointFace = cvPoint(face[0], face[1])
				endPointFace = cvPoint(face[2], face[3])
				rectanglePointList.append ([initPointFace, endPointFace])

				if self.drawFeatures:
					features = self.getFeatures(cvGetSubRect(self.grayframe, cvRect(face[0],face[1],face[4],face[5])))
					for feat in features:
						initPoint = cvPoint(face[0]+feat[0], face[1]+feat[1])
						endPoint = cvPoint(face[0]+feat[0]+feat[2], face[1]+feat[1]+feat[3])
						rectanglePointList.append ([initPoint, endPoint])

		if self.gray:
			for p in rectanglePointList:
				cvRectangle(self.grayframe, p[0], p[1], 255, 2, 8, 0)
			cvCvtColor(self.grayframe,self.image, CV_GRAY2BGR)
		else:
			for p in rectanglePointList:
				cvRectangle(self.image, p[0], p[1], CV_RGB(0, 255, 0), 2, 8, 0)
			cvCvtColor(self.image,self.image, CV_BGR2RGB)

		return gtk.gdk.pixbuf_new_from_data(self.image.imageData,gtk.gdk.COLORSPACE_RGB,0,8,self.frameWidth, self.frameHeight,self.image.widthStep)

	def getFaces(self):
		""" Obtiene la localizacion de las caras
		Devuelve una lista con la ubicacion de las caras detectadas en la imagen """
		self.getFaceLocations()
		return self.faceLocationList
		

	def getFeatures(self, img):
		""" Obtiene los rasgos de las caras

		\param img Imagen sobre la que detectar los rasgos, normalmente un SubRect.

		Devuelve una lista con la ubicacion de los rasgos (ojos, nariz y boca) detectados en la imagen. El parametro img deberia ser el SubRect de la imagen original en el que se ha detectado una cara. """

		size = cvGetSize(img)
		width = size.width

		size_2 = width >> 1
		size_4 = width >> 2
		size_8 = width >> 3
		size_16 = width >> 4
		size_32 = width >> 5

		hwindow = size_8+size_16
		w_eye_window = size_4+size_32

		imgY=cvCreateImage(cvSize(width, width), 8, 1)
		cvSobel(img, imgY, 0, 1, 3) 

		ojo_d = self.__franjaMax(imgY,hwindow, w_eye_window, width/6, width/6, size_2)
		ojo_i = self.__franjaMax(imgY,hwindow, w_eye_window, size_2+size_16, width/6, size_2)
		nariz = self.__franjaMax(imgY,hwindow, size_4, size_2 - size_8, size_2, width-width/3.75 )
		boca = self.__franjaMax(imgY,hwindow, size_2, size_4, nariz[1]+nariz[3], width-size_16)

		return [ojo_d, ojo_i, nariz, boca]


	def __franjaMax (self, img, alto, ancho, x_ini, y_ini, y_fin):
		""" Obtiene la ubicacion de la ventana de valor maximo.
		\param img Subrectangulo de la imagen sobre el que hallar la ventana
		\param alto Altura de la ventana
		\param ancho Anchura de la ventana
		\param x_ini Posicion X de la ventana
		\param y_ini Posicion Y inicial de la ventana
		\param y_fin Posicion Y final de la ventana

		Obtiene la ubicacion de la ventana (franja) de valor maximo de desplazandola en el eje Y en una zona determinada de una imagen """
		
		max=0
		y_max_franja=y_ini

		for i in range(y_ini, y_fin-alto):
			valor_franja = cvSum(cvGetSubRect(img, cvRect(x_ini,i,ancho,alto)))
			if valor_franja[0]>=max:
				max = valor_franja[0]
				y_max_franja = i

		return x_ini,y_max_franja,ancho,alto

