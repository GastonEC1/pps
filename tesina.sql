create database tesina;
use tesina;
CREATE TABLE viajes (
    Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Fecha DATE NOT NULL,
    Destino VARCHAR(150) NOT NULL,
    Tipo VARCHAR(100) NOT NULL,
    Vendedor VARCHAR(100) NOT NULL,
    Precio FLOAT NOT NULL,
    Caracteristicas VARCHAR(255) NOT NULL,
    Hospedaje VARCHAR(150) NOT NULL
);

CREATE TABLE Cliente (
    Dni INT PRIMARY KEY NOT NULL,
    Nom_ape VARCHAR(150) NOT NULL,
    Fecha_Nac DATE NOT NULL,
    Domicilio VARCHAR(150) NOT NULL,
    Discapacidad VARCHAR(100) NOT NULL,
    Correo VARCHAR(100) NOT NULL,
    Tel VARCHAR(100) NOT NULL
);

CREATE TABLE viaje_cliente (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    viaje_id INT NOT NULL,
    cliente_dni INT NOT NULL,
    FOREIGN KEY (viaje_id) REFERENCES viajes(Id),
    FOREIGN KEY (cliente_dni) REFERENCES Cliente(Dni)
);

CREATE TABLE Institucional (
    Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Nombre VARCHAR(150) NOT NULL,
    Tipo VARCHAR(50) NOT NULL,
    Direccion VARCHAR(150) NOT NULL,
    Tel VARCHAR(100) NOT NULL,
    Correo VARCHAR(100) NOT NULL
);

CREATE TABLE viaje_institucional (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    viaje_id INT NOT NULL,
    institucional_id INT NOT NULL,
    FOREIGN KEY (viaje_id) REFERENCES viajes(Id) ,
    FOREIGN KEY (institucional_id) REFERENCES Institucional(Id) 
);


CREATE TABLE Caja (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('ingreso', 'egreso') NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha DATETIME NOT NULL,
    descripcion VARCHAR(255),
    viaje_id INT NULL,
    FOREIGN KEY (viaje_id) REFERENCES viajes(Id)
);

CREATE TABLE Coordinadores (
    Dni INT PRIMARY KEY,
    Nom_ape VARCHAR(150) NOT NULL,
    Tel VARCHAR(100) NOT NULL,
    Direccion VARCHAR(150) NOT NULL,
    fecha_nac DATE NOT NULL
);

CREATE TABLE viaje_coordinador (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    viaje_id INT NOT NULL,
    coordinador_id INT NOT NULL,
    FOREIGN KEY (viaje_id) REFERENCES viajes(Id) ,
    FOREIGN KEY (coordinador_id) REFERENCES Coordinadores(Dni)
);

CREATE TABLE Jugadores (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(150) NOT NULL,
    Tipo VARCHAR(100) NOT NULL,
    Fecha_Nac DATE NOT NULL,
    Direccion VARCHAR(150) NOT NULL,
    Tel VARCHAR(100) NOT NULL,
    Correo VARCHAR(100) NOT NULL,
    Institucional_Id INT NOT NULL,
    FOREIGN KEY (Institucional_Id) REFERENCES Institucional(Id)
);

ALTER TABLE Jugadores
ADD COLUMN Dni VARCHAR(20) NOT NULL;

ALTER TABLE viajes
ADD COLUMN Comida varchar(20) NOT NULL;

ALTER TABLE viajes
DROP COLUMN Comida;

ALTER TABLE viajes ADD COLUMN estado VARCHAR(10) DEFAULT 'Pendiente';

