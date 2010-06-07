#!/usr/bin/python
""" @package InterfazReconocimiento """

from math import exp, cos, sin
from Exceptions import *

try:
	from opencv.cv import *
	from opencv.highgui import *
except:
	raise OpenCVLibraryNotFoundException()


def getFeatures(img):

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

	ojo_d = __franjaMax(imgY,hwindow, w_eye_window, width/6, width/6, size_2)
	ojo_i = __franjaMax(imgY,hwindow, w_eye_window, size_2+size_16, width/6, size_2)
	nariz = __franjaMax(imgY,hwindow, size_4, size_2 - size_8, size_2, width-width/3.75 )
	boca = __franjaMax(imgY,hwindow, size_2, size_4, nariz[1]+nariz[3], width-size_16)

	return [ojo_d, ojo_i, nariz, boca]


def __franjaMax (img, alto, ancho, x_ini, y_ini, y_fin):
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

def gaborFiltering(image, kernels):

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

		cvConvertScale(dest, img_aux, 255.0)
		cvCopy(img_aux, cvGetSubRect(img_total,cvRect(i*img_aux.width,0,img_aux.width,img_aux.height)))
		i+=1

	cvSaveImage("cosa.png", img_total)


class FaceSignature:
	""" Caracteristicas del individuo """

	def __init__(self, img):
		return None
		
if __name__=="__main__":
	kernels = createGaborKernels(range(0,360,60))
	img = cvLoadImage("./resources/NoImage.jpg")
	img_aux = cvCreateImage(cvSize(img.width,img.height),IPL_DEPTH_8U,1)

	cvCvtColor(img,img_aux,CV_RGB2GRAY)

	gaborFiltering(img_aux, kernels)

