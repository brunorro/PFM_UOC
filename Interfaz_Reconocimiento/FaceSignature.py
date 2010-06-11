#!/usr/bin/python
""" @package InterfazReconocimiento """

from math import exp, cos, sin
from Exceptions import *
import gtk

try:
	from opencv.cv import *
	from opencv.highgui import *
except:
	raise OpenCVLibraryNotFoundException()


def getFeatures(img):
	""" Busca la ubicacion de los rasgos
	\param img Imagen de la que encontrar los rasgos
	Devuelve la ubicacion de los rasgos faciales, buscando las franjas maximas 
	"""

	size = cvGetSize(img)
	width = size.width
	#height= size.height

	size_2 = width >> 1
	size_4 = width >> 2
	size_8 = width >> 3
	size_16 = width >> 4
	size_32 = width >> 5

	hwindow = size_8+size_16
	w_eye_window = size_4+size_32

	imgY=cvCreateImage(cvSize(width, width), 8, 1)
	#imgY=cvCreateImage(cvSize(width, height), 8, 1)
	cvSobel(img, imgY, 0, 1, 3) 

	ojo_d = __franjaMax(imgY,hwindow, w_eye_window, width/6, width/6, size_2)
	ojo_i = __franjaMax(imgY,hwindow, w_eye_window, size_2+size_16, width/6, size_2)
	nariz = __franjaMax(imgY,hwindow, size_4, size_2 - size_8, size_2, width-width/3.75 )
	boca = __franjaMax(imgY,hwindow, size_2, size_4, nariz[1]+nariz[3], width-size_16)

	return ojo_d, ojo_i, nariz, boca

def __franjaMax (img, alto, ancho, x_ini, y_ini, y_fin):
	""" Obtiene la ubicacion de la ventana de valor maximo.
	\param img Imagen sobre el que hallar la ventana
	\param alto Altura de la ventana
	\param ancho Anchura de la ventana
	\param x_ini Posicion X de la ventana
	\param y_ini Posicion Y inicial de la ventana
	\param y_fin Posicion Y final de la ventana

	Obtiene la ubicacion (Xinicial, Yinicial, anchura, altura) de la ventana (franja) de valor maximo de desplazandola en el eje Y en una zona determinada de una imagen """
		
	max=0
	y_max_franja=y_ini

	for i in range(y_ini, y_fin-alto):
		valor_franja = cvSum(cvGetSubRect(img, cvRect(x_ini,i,ancho,alto)))
		if valor_franja[0]>=max:
			max = valor_franja[0]
			y_max_franja = i

	return x_ini,y_max_franja,ancho,alto

def createGaborKernels (inclinations=[0,30,60,90,120,150],kernel_size=9,pos_var=16,pos_w=10, pos_psi=90):
	""" Crea kernels para el pase por un filtro de Gabor
	\param inclinations Array de inclinaciones (por defecto son 0,30,60,90,120 y 150 grados)
	\param kernel_size Tamanyo del kernel a concatenar. Por defecto 9. Trunca al siguiente numero impar.
	\pos_var Variancia de la gaussiana empleada para generar los kernels
	\pos_w Parametro Omega para el kernel del filtro de Gabor
	\pos_psi Parametro Psi para el kernel del filtro de Gabor """

	if kernel_size%2==0:
		kernel_size+=1

	resultKernels = []

	for pos_phase in inclinations:
		var = pos_var/10.0
		w = pos_w/10.0
		phase = pos_phase*CV_PI/180.0
		psi = CV_PI*pos_psi/180.0
 
		kernel = cvCreateMat(kernel_size,kernel_size,CV_32FC1)
		cvZero(kernel)

		for x in range(-kernel_size/2+1,kernel_size/2+1):
        		for y in range(-kernel_size/2+1,kernel_size/2+1):
				kernel_val = exp( -((x*x)+(y*y))/(2*var))*cos( w*x*cos(phase)+w*y*sin(phase)+psi)
				cvSet2D(kernel,y+kernel_size/2,x+kernel_size/2,cvScalar(kernel_val))

		resultKernels.append(kernel)

	return resultKernels

def gaborFilteringConcat(image, kernels):
	""" Devuelve una imagen filtrada con el banco de filtros de Gabor, concatenadas por cada filtrado
	\param image Imagen de la que sacar el filtrado de Gabor
	\param kernels Matriz con los kernels de Gabor con los que se llevara a cabo el banco de filtros
	"""

	cvEqualizeHist(image,image)
	src_f = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_32F,1)
	cvConvertScale(image,src_f,1.0/255)

	dest = cvCloneImage(src_f)
	dest_mag = cvCloneImage(src_f)
	img_aux = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_8U, 1)
	img_total = cvCreateImage(cvSize(len(kernels)*image.width,image.height),IPL_DEPTH_8U, 1)

	i=0
	for k in kernels:
		cvFilter2D(src_f, dest,k,cvPoint(-1,-1))
		cvPow(dest,dest_mag,2)
		cvZero(img_aux)

		cvConvertScale(dest, img_aux, 255.0)
		cvCopy(img_aux, cvGetSubRect(img_total,cvRect(i*img_aux.width,0,img_aux.width,img_aux.height)))
		i+=1

	cvSmooth(img_total,img_total)
	cvThreshold(img_total, img_total, 16, 255, CV_THRESH_BINARY)

	return img_total


def gaborFilteringSuperp(image, kernels):
	""" Devuelve una imagen filtrada con el banco de filtros de Gabor, concatenadas por cada filtrado
	\param image Imagen de la que sacar el filtrado de Gabor
	\param kernels Matriz con los kernels de Gabor con los que se llevara a cabo el banco de filtros
	"""

	cvEqualizeHist(image,image)
	src_f = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_32F,1)
	cvConvertScale(image,src_f,1.0/255)

	dest = cvCloneImage(src_f)
	dest_mag = cvCloneImage(src_f)
	img_aux = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_8U, 1)
	img_total = cvCreateImage(cvSize(image.width,image.height),IPL_DEPTH_8U, 1)
	cvZero(img_aux)
	cvZero(img_total)

	i=0
	for k in kernels:
		cvFilter2D(src_f, dest,k,cvPoint(-1,-1))
		cvPow(dest,dest_mag,2)
		cvZero(img_aux)

		cvConvertScale(dest, img_aux, 255.0/len(kernels))
		cvAdd(img_aux, img_total, img_total)
		i+=1

	cvSmooth(img_total,img_total)
	cvThreshold(img_total, img_total, 16, 255, CV_THRESH_BINARY)

	return img_total


class FaceSignature:
	""" Caracteristicas del individuo """
	slicePointEuc = [87.0, 85.0, 100.5, 112.5]
	slicePointXor = [0.44, 0.44, 0.48, 0.59]
	slicePointAnd = [0.49, 0.45, 0.49, 0.41]

	def __init__(self, img=None):

		self.gaborKernels = createGaborKernels(range(0,180,10))

		if img!=None:
			[rightEyePos, leftEyePos, nosePos, mouthPos] = getFeatures(img)
	
			imgRightEyeAux = cvGetSubRect(img,cvRect(rightEyePos[0],rightEyePos[1],rightEyePos[2],rightEyePos[3]))
			imgLeftEyeAux = cvGetSubRect(img,cvRect(leftEyePos[0],leftEyePos[1],leftEyePos[2],leftEyePos[3]))
			imgNoseAux = cvGetSubRect(img,cvRect(nosePos[0],nosePos[1],nosePos[2],nosePos[3]))
			imgMouthAux = cvGetSubRect(img,cvRect(mouthPos[0],mouthPos[1],mouthPos[2],mouthPos[3]))

			self.signRightEye = gaborFilteringSuperp(imgRightEyeAux, self.gaborKernels)
			self.signLeftEye= gaborFilteringSuperp(imgLeftEyeAux, self.gaborKernels)
			self.signNose= gaborFilteringSuperp(imgNoseAux, self.gaborKernels)
			self.signMouth = gaborFilteringSuperp(imgMouthAux, self.gaborKernels)

	def setFromImage(self, img):
		[rightEyePos, leftEyePos, nosePos, mouthPos] = getFeatures(img)
	
		imgRightEyeAux = cvGetSubRect(img,cvRect(rightEyePos[0],rightEyePos[1],rightEyePos[2],rightEyePos[3]))
		imgLeftEyeAux = cvGetSubRect(img,cvRect(leftEyePos[0],leftEyePos[1],leftEyePos[2],leftEyePos[3]))
		imgNoseAux = cvGetSubRect(img,cvRect(nosePos[0],nosePos[1],nosePos[2],nosePos[3]))
		imgMouthAux = cvGetSubRect(img,cvRect(mouthPos[0],mouthPos[1],mouthPos[2],mouthPos[3]))

		self.signRightEye = gaborFilteringSuperp(imgRightEyeAux, self.gaborKernels)
		self.signLeftEye= gaborFilteringSuperp(imgLeftEyeAux, self.gaborKernels)
		self.signNose= gaborFilteringSuperp(imgNoseAux, self.gaborKernels)
		self.signMouth = gaborFilteringSuperp(imgMouthAux, self.gaborKernels)

	def getPixbufSignature(self):
		imgWidth = self.signRightEye.width+self.signLeftEye.width+self.signNose.width+self.signMouth.width
		imageSignatures = cvCreateImage(cvSize(imgWidth,self.signMouth.height), IPL_DEPTH_8U, 1)
		imagePixbuf = cvCreateImage(cvSize(imgWidth,self.signMouth.height), IPL_DEPTH_8U, 3)

		cvCopy(self.signRightEye, cvGetSubRect(imageSignatures, cvRect(0,0,self.signRightEye.width,self.signRightEye.height)))
		offset = self.signRightEye.width
		cvCopy(self.signLeftEye, cvGetSubRect(imageSignatures, cvRect(offset,0,self.signLeftEye.width,self.signLeftEye.height)))
		offset +=self.signLeftEye.width
		cvCopy(self.signNose, cvGetSubRect(imageSignatures, cvRect(offset,0,self.signNose.width,self.signNose.height)))
		offset +=self.signNose.width
		cvCopy(self.signMouth, cvGetSubRect(imageSignatures, cvRect(offset,0,self.signMouth.width,self.signMouth.height)))

		cvCvtColor(imageSignatures,imagePixbuf ,CV_GRAY2RGB)
		return gtk.gdk.pixbuf_new_from_data(imagePixbuf.imageData,gtk.gdk.COLORSPACE_RGB,0,8,imagePixbuf.width, imagePixbuf.height,imagePixbuf.widthStep)


	def loadSignature(self, fileNames):
		if len(fileNames)<4:
			self.signRightEye = None
			self.signLeftEye = None
			self.signNose = None
			self.signMouth = None

		else:
			signOrigArray = []
			for fileSign in fileNames:
				signOrig = cvLoadImage(fileSign)

				if signOrig.nChannels > 1:
					imgAux = cvCreateImage(cvSize(signOrig.width, signOrig.height), IPL_DEPTH_8U, 1)
					cvCvtColor(signOrig,imgAux,CV_RGB2GRAY)

				signOrigArray.append(imgAux)
				
			self.signRightEye = signOrigArray[0]
			self.signLeftEye =  signOrigArray[1]
			self.signNose =  signOrigArray[2]
			self.signMouth =  signOrigArray[3]

	def saveSignature(self, fileName):
		cvSaveImage(fileName+"_od.png", self.signRightEye)
		cvSaveImage(fileName+"_oi.png", self.signLeftEye)
		cvSaveImage(fileName+"_n.png", self.signNose)
		cvSaveImage(fileName+"_b.png", self.signMouth)
			
	def compareSignatureEuc(self, facePrint):
		diffMatRightEye = cvCloneImage(self.signRightEye)
		diffMatLeftEye = cvCloneImage(self.signLeftEye)
		diffMatNose = cvCloneImage(self.signNose)
		diffMatMouth = cvCloneImage(self.signMouth)

		cvAbsDiff(self.signRightEye, facePrint.signRightEye, diffMatRightEye)
		cvAbsDiff(self.signLeftEye, facePrint.signLeftEye, diffMatLeftEye)
		cvAbsDiff(self.signNose, facePrint.signNose, diffMatNose)
		cvAbsDiff(self.signMouth, facePrint.signMouth, diffMatMouth)

		return cvSum(diffMatRightEye)[0]/(diffMatRightEye.width*diffMatRightEye.height),\
			cvSum(diffMatLeftEye)[0]/(diffMatLeftEye.width*diffMatLeftEye.height),\
			cvSum(diffMatNose)[0]/(diffMatNose.width*diffMatNose.height),\
			cvSum(diffMatMouth)[0]/(diffMatMouth.width*diffMatMouth.height)

	def compareSignatureXor(self, facePrint):
		xorMatRightEye = cvCloneImage(self.signRightEye)
		xorMatLeftEye = cvCloneImage(self.signLeftEye)
		xorMatNose = cvCloneImage(self.signNose)
		xorMatMouth = cvCloneImage(self.signMouth)

		cvXor(self.signRightEye, facePrint.signRightEye, xorMatRightEye )
		cvXor(self.signLeftEye, facePrint.signLeftEye, xorMatLeftEye )
		cvXor(self.signNose, facePrint.signNose,  xorMatNose )
		cvXor(self.signMouth, facePrint.signMouth,  xorMatMouth)

		orMatRightEye = cvCloneImage(self.signRightEye)
		orMatLeftEye = cvCloneImage(self.signLeftEye)
		orMatNose = cvCloneImage(self.signNose)
		orMatMouth = cvCloneImage(self.signMouth)

		cvOr(self.signRightEye, facePrint.signRightEye,  orMatRightEye )
		cvOr(self.signLeftEye, facePrint.signLeftEye,  orMatLeftEye )
		cvOr(self.signNose, facePrint.signNose,  orMatNose )
		cvOr(self.signMouth, facePrint.signMouth,  orMatMouth )

		return cvSum(xorMatRightEye)[0]/cvSum(orMatRightEye)[0],\
			cvSum(xorMatLeftEye)[0]/cvSum(orMatLeftEye)[0],\
			cvSum(xorMatNose)[0]/cvSum(orMatNose)[0],\
			cvSum(xorMatMouth)[0]/cvSum(orMatMouth)[0]

	def compareSignatureAnd(self, facePrint):
		andMatRightEye = cvCloneImage(self.signRightEye)
		andMatLeftEye = cvCloneImage(self.signLeftEye)
		andMatNose = cvCloneImage(self.signNose)
		andMatMouth = cvCloneImage(self.signMouth)

		cvAnd(self.signRightEye, facePrint.signRightEye, andMatRightEye )
		cvAnd(self.signLeftEye, facePrint.signLeftEye, andMatLeftEye )
		cvAnd(self.signNose, facePrint.signNose,  andMatNose )
		cvAnd(self.signMouth, facePrint.signMouth,  andMatMouth)

		orMatRightEye = cvCloneImage(self.signRightEye)
		orMatLeftEye = cvCloneImage(self.signLeftEye)
		orMatNose = cvCloneImage(self.signNose)
		orMatMouth = cvCloneImage(self.signMouth)

		cvOr(self.signRightEye, facePrint.signRightEye, orMatRightEye )
		cvOr(self.signLeftEye, facePrint.signLeftEye, orMatLeftEye )
		cvOr(self.signNose, facePrint.signNose, orMatNose )
		cvOr(self.signMouth, facePrint.signMouth, orMatMouth )

		return cvSum(andMatRightEye)[0]/cvSum(orMatRightEye)[0],\
			cvSum(andMatLeftEye)[0]/cvSum(orMatLeftEye)[0],\
			cvSum(andMatNose)[0]/cvSum(orMatNose)[0],\
			cvSum(andMatMouth)[0]/cvSum(orMatMouth)[0]



