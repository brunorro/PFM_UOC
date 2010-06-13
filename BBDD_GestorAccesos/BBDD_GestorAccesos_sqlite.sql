CREATE TABLE IF NOT EXISTS Empresa (
	idEmpresa INTEGER PRIMARY KEY, 
	nombreEmpresa VARCHAR(32) UNIQUE NOT NULL);

INSERT INTO Empresa (nombreEmpresa) VALUES ('ACME');

CREATE TABLE IF NOT EXISTS Sede (
	idSede INTEGER PRIMARY KEY,
	idEmpresa INTEGER CONSTRAINT fkSedeEmpresa 
		REFERENCES Empresa(idEmpresa) ON DELETE RESTRICT, 
	nombreSede VARCHAR(32) NOT NULL, 
	l1DireccionSede VARCHAR(64) DEFAULT NULL, 
	l2DireccionSede VARCHAR(64) DEFAULT NULL, 
	tlfSede VARCHAR(14) DEFAULT NULL, 
	faxSede VARCHAR(14) DEFAULT NULL,
		CONSTRAINT fkIDSede UNIQUE (idEmpresa, idSede));

INSERT INTO Sede (idEmpresa, nombreSede) VALUES (0, 'ACME-Sede1');
INSERT INTO Sede (idEmpresa, nombreSede) VALUES (0, 'ACME-Sede2');

CREATE TABLE IF NOT EXISTS Departamento (
	idDepartamento INTEGER PRIMARY KEY,
	idEmpresa INTEGER CONSTRAINT fkDepartamentoEmpresa 
		REFERENCES Empresa(idEmpresa), 
	nombreDepartamento VARCHAR(16) NOT NULL,
	responsableDepartamento INTEGER DEFAULT NULL);

INSERT INTO Departamento (idEmpresa, idDepartamento, nombreDepartamento) 
	VALUES (0,0,'Dirección');
INSERT INTO Departamento (idEmpresa, idDepartamento, nombreDepartamento) 
	VALUES (0,1,'Producción');
INSERT INTO Departamento (idEmpresa, idDepartamento, nombreDepartamento) 
	VALUES (0,2,'I+D');

CREATE TABLE IF NOT EXISTS Empleado (
	idEmpleado INTEGER PRIMARY KEY,
	idEmpresa INTEGER CONSTRAINT fkEmpleadoEmpresa
		REFERENCES Empresa(idEmpresa) ON DELETE RESTRICT,
	idDepartamento INTEGER CONSTRAINT fkEmpleadoDepartamento
		REFERENCES Departamento(idDepartamento) ON DELETE RESTRICT,
	nifEmpleado VARCHAR(9) UNIQUE NOT NULL,
	nombreEmpleado VARCHAR(32) NOT NULL,
	apellidosEmpleado VARCHAR(64) NOT NULL,
	l1DireccionEmpleado VARCHAR(64) DEFAULT NULL,
	l2DireccionEmpleado VARCHAR(64) DEFAULT NULL,
	tlf1Empleado VARCHAR(14) DEFAULT NULL,
	tlf2Empleado VARCHAR(14) DEFAULT NULL,
	mailEmpleado VARCHAR(14) DEFAULT NULL, 
	imagenEmpleado VARCHAR(255) DEFAULT NULL);

INSERT INTO Empleado (idEmpresa, idDepartamento, nifEmpleado, nombreEmpleado, 
	apellidosEmpleado, imagenEmpleado) VALUES (0,0,'00000000A','E1','A1', 'resources/imgEmployees/00000000A.jpg');
INSERT INTO Empleado (idEmpresa, idDepartamento, nifEmpleado, nombreEmpleado, 
	apellidosEmpleado) VALUES (0,0,'00000001B','E2','A2');
INSERT INTO Empleado (idEmpresa, idDepartamento, nifEmpleado, nombreEmpleado, 
	apellidosEmpleado) VALUES (0,0,'00000002C','E3','A3');
INSERT INTO Empleado (idEmpresa, idDepartamento, nifEmpleado, nombreEmpleado, 
	apellidosEmpleado) VALUES (0,0,'00000003D','E4','A4');


CREATE TABLE IF NOT EXISTS Fichaje (
	idEmpleado INTEGER CONSTRAINT fkFichajeEmpleado
		REFERENCES Empleado(idEmpleado),
	idSede INTEGER CONSTRAINT fkFichajeSede
		REFERENCES Sede (idSede),
	fechaFichaje INTEGER NOT NULL);


INSERT INTO Fichaje (idEmpleado, idSede, fechaFichaje) values (0,0,1269625799);
INSERT INTO Fichaje (idEmpleado, idSede, fechaFichaje) values (2,0,1269626090);

INSERT INTO Fichaje (idEmpleado, idSede, fechaFichaje) values (1,0,1269626000);
INSERT INTO Fichaje (idEmpleado, idSede, fechaFichaje) values (1,0,1269626999);
INSERT INTO Fichaje (idEmpleado, idSede, fechaFichaje) values (1,0,1269638990);
INSERT INTO Fichaje (idEmpleado, idSede, fechaFichaje) values (1,0,1269631200);
