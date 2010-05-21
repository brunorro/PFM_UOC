#!/usr/bin/python
import sqlite3
#from DbDriver import *

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

	def getEmployeeData(self, employeeId):
		return self.__executeQuery ('SELECT * from empleado where idEmpleado='+str(employeeId))[0]

	def getEmployeeClocks(self, employeeId):
		return self.__executeQuery ('SELECT * from Fichaje where idEmpleado='+str(employeeId)+' ORDER BY fechaFichaje')
		

if __name__=="__main__":
	driver = SqliteDriver("../BBDD_GestorAccesos/GestorAccesos.bd")
	driver.getEmployees()
