#!/usr/bin/python
import sqlite3
import datetime, time

class SqliteDriver():
	def __init__(self, DBFile):
		self.DBFile = DBFile
		self.conn = sqlite3.connect(self.DBFile)

	def setParameters(self, DBFile):
		self.DBFile = DBFile

	def connect(self):
		self.conn = sqlite3.connect(self.DBFile)

	def __executeQuery(self, query):
		c = self.conn.cursor()
		c.execute (query)
		result = c.fetchall()
		self.conn.commit()
		c.close()
		return result

	def getEmployeeList(self):
		return self.__executeQuery ('''SELECT * from empleado''')

	def getDepartmentList(self):
		return self.__executeQuery ('''SELECT * from Departamento ''')

	def getEmployeeData(self, employeeId):
		return self.__executeQuery ('SELECT * from empleado where idEmpleado='+str(employeeId))[0]

	def getEmployeeClocks(self, employeeId):
		return self.__executeQuery ('SELECT * from Fichaje where idEmpleado='+str(employeeId)+' ORDER BY fechaFichaje')

	def getReport (self, employeeIdFrom, employeeIdTo, departmentFrom, departmentTo, dateFrom, dateTo):
		datetimeFrom = datetime.datetime(dateFrom[0],dateFrom[1]+1,dateFrom[2],00,00,00)
		datetimeTo = datetime.datetime(dateTo[0],dateTo[1]+1,dateTo[2],23,59,59)

		stampFrom = int(time.mktime(datetimeFrom.timetuple()))
		stampTo = int(time.mktime(datetimeTo.timetuple()))

		print "select * from Fichaje where idEmpleado between %d and %d and fechaFichaje between %d and %d" % (employeeIdFrom, employeeIdTo, stampFrom, stampTo)

		return self.__executeQuery ("select * from Fichaje where idEmpleado between %d and %d and fechaFichaje between %d and %d" % (employeeIdFrom, employeeIdTo, stampFrom, stampTo))
		

