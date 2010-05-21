#!/usr/bin/python
import time 

try:
	import gtk, pygtk
	pygtk.require("2.0")
except:
	print ("No se encontro la libreria grafica GTK")
	sys.exit(1)


class MainWindow:
	def __init__(self, mainClass):
		self.mainClass= mainClass

		self.builder = gtk.Builder()
		self.builder.add_from_file("./resources/MainWindow.glade")

		self.window = self.builder.get_object("MainWindow")
		self.__getWidgets()
		self.__initSectionsTree()
		
		self.builder.connect_signals(self)

	def on_MainWindow_destroy(self, widget, data=None):
		self.mainClass.quit()

	def on_MainImagemenuitemQuit_activate(self, widget, data=None):
		self.reportDialog.show()
		#self.mainClass.quit()

	def __getWidgets(self):
		self.mainStatusbar = self.builder.get_object("MainStatusbar")
		self.mainStatusbar.push(0,"Bienvenido")

		self.sectionTreeview = self.builder.get_object("SectionTreeview")
		self.sectionTreestore = self.builder.get_object("SectionTreestore")

		self.mainNotebook = self.builder.get_object("MainNotebook")

		self.employeeNameEntry = self.builder.get_object("EmployeeNameEntry")
		self.employeeIdEntry = self.builder.get_object("EmployeeIdEntry")
		self.employeeAddressEntry = self.builder.get_object("EmployeeAddressEntry")
		self.employeePhoneEntry = self.builder.get_object("EmployeePhoneEntry")
		self.employeeMailEntry = self.builder.get_object("EmployeeMailEntry")
		self.employeeAccessListStore = self.builder.get_object("EmployeeAccessListStore")

	def __initSectionsTree(self):
		employeeParentEntry = self.sectionTreestore.append(None,["Empleados", -1])
		employeeReportsEntry = self.sectionTreestore.append(None,["Listados", -2])

		employeeList = self.mainClass.dbDriver.getEmployeeList()

		for row in employeeList:
			treeIterAux = self.sectionTreestore.append(employeeParentEntry,["%s, %s" % (row[5], row[4]), row[0]])

		self.sectionTreestore.append(employeeReportsEntry, ["Ultimo dia", 0])
		self.sectionTreestore.append(employeeReportsEntry, ["Ultima semana", 0])
		self.sectionTreestore.append(employeeReportsEntry, ["Acumulado por tiempo", 0])


	def on_treeview_button_press_event(self,treeview,path,column):
		iter = self.sectionTreestore.get_iter(path)
		employeeId = self.sectionTreestore.get(iter,1)[0]

		parentIter = self.sectionTreestore.iter_parent(iter)
		parentValue = self.sectionTreestore.get(parentIter,0)[0]

		if parentValue=="Empleados" and len(path)>1:
			employeeData = self.mainClass.dbDriver.getEmployeeData(employeeId)
			employeeAccesses = self.mainClass.dbDriver.getEmployeeClocks(employeeId)
			self.fillEmployeeData(employeeData,employeeAccesses)
			self.mainNotebook.set_current_page(0)

		elif parentValue=="Listados" and len(path)>1:
			self.mainNotebook.set_current_page(1)

		return 1

	def fillEmployeeData(self, employeeData, employeeAccesses):

		self.employeeNameEntry.set_text("%s %s" %(employeeData[4], employeeData[5]))
		self.employeeIdEntry.set_text("%s" % (employeeData[3]))
		self.employeeAddressEntry.set_text("%s %s" % (employeeData[6], employeeData[7]))
		self.employeePhoneEntry.set_text("%s" % (employeeData[8]))
		self.employeeMailEntry.set_text("%s" % (employeeData[9]))

                self.employeeAccessListStore.clear()

		for row in employeeAccesses:
			if row[2] is None:
				exitTime = None
				difference = 0
			else:
				exitTime = time.ctime(row[2])
				hoursDifference= row[3]/3600
				minsDifference= (row[3]%3600)/60
				secsDifference= (row[3]%3600)%60
				difference = "%02d %02d %02d" % (hoursDifference,minsDifference,secsDifference)

			self.employeeAccessListStore.append([row[0], time.ctime(row[1]), exitTime, difference])

		return 1

	def on_EmployeeButtonModify_clicked(self, widget, data=None):
		self.mainStatusbar.push(0, "Boton modificar pulsado")
		#self.setEditMode()

	def on_EmployeeButtonSave_clicked(self, widget, data=None):
		self.mainStatusbar.push(0, "Guardando")

	def on_EmployeeButtonExit_clicked(self, widget, data=None):
		self.mainStatusbar.push(0, "Abortando cambios")
		#self.setViewMode()


