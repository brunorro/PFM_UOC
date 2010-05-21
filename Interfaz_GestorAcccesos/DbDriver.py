#!/usr/bin/python

from SqliteDriver import *

class DbDriver:
	def __init__(self, dbType, params):
		if dbType=="SQLITE":
			for options in params:
				if options[0]=="dbFile":
					self.driver = SqliteDriver(options[1])
			
		if dbType=="POSTGRESQL":
			self.driver = None

	def getEmployeeList(self):
		return self.driver.getEmployeeList()

	def getEmployeeData(self, employeeID):
		return self.driver.getEmployeeData(employeeID)

	def getEmployeeClocks(self, employeeID):
		returnList = []
		ClockList = self.driver.getEmployeeClocks(employeeID)
		i = 0
		for row in ClockList:
			if not i&1: # Modulo rapido
				returnList.append([row[0], row[2], None, 0])
			else :
				returnList[i>>1][2]=row[2]
				returnList[i>>1][3]=returnList[i>>1][2]-returnList[i>>1][1]
			i+=1
		return returnList
			

if __name__=="__main__":
	params = ('SQLITE', '../BBDD_GestorAccesos/GestorAccesos.bd')
	dbDriver = DbDriver(params)
	dbDriver.getEmployees()
