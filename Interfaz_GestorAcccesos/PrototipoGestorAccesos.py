#!/usr/bin/env python
## @package GestorAccesos
#
# Aplicacion de gestion de accesos.

import gtk, pygtk
import locale, gettext

from MainWindow import *
from DbDriver import *
from Configuration import *

## Punto de entrada a la aplicacion
#
# La clase GestorAccesos es el punto de entrada a la aplicacion de gestion de accesos. Desde ella se lee la configuracion, se abre la base de datos y se llama a la interfaz grafica
class GestorAccesos:

	## Constructor de la clase
	#
	# En la clase constructora se realiza, en el siguiente orden:
	# \li Carga de la configuracion y obtencion de los parametros de la base de datos de este
	# \li Invocacion al objeto DbDriver con la informacion de la configuracion obtenida previamente
	# \li Invocacion de la ventana principal
	# La ventana principal ejecuta los metodos del objeto DbDriver instanciado en esta clase para realizar todas las consultas
	def __init__(self):
		locale.setlocale(locale.LC_ALL, '')
		gettext.bindtextdomain("GestorAccesos", ".")
		gettext.textdomain("GestorAccesos")
		_ = gettext.gettext

		self.appConfig = Configuration("resources/prueba.xml")
		self.appConfig.getDbConfiguration()
		self.dbDriver = DbDriver(self.appConfig.dbType, self.appConfig.dbParams)

		mgui = MainWindow(self)
		mgui.window.show()
		gtk.main()

	## Funcion para la salida de la aplicacion
	#
	# Funcion para la salida de la aplicacion.
	def quit(self):
		gtk.main_quit()
	
if __name__ == "__main__":
	gestorAccesos = GestorAccesos()
