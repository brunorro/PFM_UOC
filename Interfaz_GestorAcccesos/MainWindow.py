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
		self.__refreshEmployeeComboListStore()
		self.__refreshDepartmentComboListStore()

		self.builder.connect_signals(self)

	def on_MainWindow_destroy(self, widget, data=None):
		self.mainClass.quit()

	def on_MainImagemenuitemQuit_activate(self, widget, data=None):
		self.mainClass.quit()

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

		self.fromEmployeeComboboxentry= self.builder.get_object("FromEmployeeComboboxentry")
		self.toEmployeeComboboxentry= self.builder.get_object("ToEmployeeComboboxentry")
		self.whereEmployeeComboboxentry= self.builder.get_object("WhereEmployeeComboboxentry")

		self.departmentFromComboboxentry = self.builder.get_object("DepartmentFromComboboxentry")
		self.departmentToComboboxentry = self.builder.get_object("DepartmentToComboboxentry")

		self.departmentComboListStore = self.builder.get_object("DepartmentComboListStore")
		self.employeeComboListStore = self.builder.get_object("EmployeeComboListStore")
                self.whereEmployeeComboListStore = self.builder.get_object("WhereEmployeeComboListStore")

		self.dateFromCalendar = self.builder.get_object("DateFromCalendar")
		self.dateToCalendar = self.builder.get_object("DateToCalendar")

                self.whereHoursEntry = self.builder.get_object("WhereHoursEntry")


	def __initSectionsTree(self):
		employeeParentEntry = self.sectionTreestore.append(None,["Empleados", -1])
		employeeReportsEntry = self.sectionTreestore.append(None,["Listados", -2])

		employeeList = self.mainClass.dbDriver.getEmployeeList()

		for row in employeeList:
			treeIterAux = self.sectionTreestore.append(employeeParentEntry,["%s, %s" % (row[5], row[4]), row[0]])

		self.sectionTreestore.append(employeeReportsEntry, ["Ultimo dia", 0])
		self.sectionTreestore.append(employeeReportsEntry, ["Ultima semana", 0])
		self.sectionTreestore.append(employeeReportsEntry, ["Acumulado por tiempo", 0])

	def __refreshEmployeeComboListStore(self):
		self.employeeComboListStore.clear()
		employeeList = self.mainClass.dbDriver.getEmployeeList()

		for row in employeeList:
			self.employeeComboListStore.append([row[0], "%s, %s" % (row[5], row[4])])

		self.fromEmployeeComboboxentry.set_active(0)
		self.toEmployeeComboboxentry.set_active(len(employeeList)-1)

	def __refreshDepartmentComboListStore(self):
		self.departmentComboListStore.clear()
		departmentList = self.mainClass.dbDriver.getDepartmentList()

		for row in departmentList:
			self.departmentComboListStore.append([row[0], row[2]])

		self.departmentFromComboboxentry.set_active(0)
		self.departmentToComboboxentry.set_active(0)


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

	def on_WhereEmployeeComboboxentry_changed(self, widget, data=None):
		whereOption = self.whereEmployeeComboboxentry.get_active_iter()

		if self.whereEmployeeComboListStore.get_value(whereOption,0)==-1:
			self.whereHoursEntry.set_property("editable", False)
		else :
			self.whereHoursEntry.set_property("editable", True)

	def on_WhereHoursEntry_changed(self, widget, data=None):
		data = self.whereHoursEntry.get_text()
		try:
			x=(int(data))
		except:
			self.whereHoursEntry.set_text("")

	def on_ReportOKButton_clicked(self, widget, data=None):
		iterAux = self.fromEmployeeComboboxentry.get_active_iter()
		if iterAux!=None: employeeIdFrom = self.employeeComboListStore.get_value(iterAux,0)
		else: employeeIdFrom = None

		iterAux = self.toEmployeeComboboxentry.get_active_iter()
		if iterAux!=None: employeeIdTo = self.employeeComboListStore.get_value(iterAux,0)
		else: employeeIdTo = None

		iterAux = self.departmentFromComboboxentry.get_active_iter()
		if iterAux!=None: departmentIdFrom = self.departmentComboListStore.get_value(iterAux,0)
		else: departmentIdFrom = None

		iterAux = self.departmentToComboboxentry.get_active_iter()
		if iterAux!=None: departmentIdTo = self.departmentComboListStore.get_value(iterAux,0)
		else: departmentIdTo = None

		iterAux = self.whereEmployeeComboboxentry.get_active_iter()
		if iterAux!=None: employeeWhere = self.whereEmployeeComboListStore.get_value(iterAux,0)
		else: employeeWhere = None

		dateFrom = self.dateFromCalendar.get_date()
		dateTo = self.dateToCalendar.get_date()

		self.mainClass.dbDriver.getReport(employeeIdFrom, employeeIdTo, departmentIdFrom, departmentIdTo, dateFrom, dateTo)

	def on_EmployeeButtonModify_clicked(self, widget, data=None):
		self.mainStatusbar.push(0, "Boton modificar pulsado")
		#self.setEditMode()

	def on_EmployeeButtonSave_clicked(self, widget, data=None):
		self.mainStatusbar.push(0, "Guardando")

	def on_EmployeeButtonExit_clicked(self, widget, data=None):
		self.mainStatusbar.push(0, "Abortando cambios")
		#self.setViewMode()


