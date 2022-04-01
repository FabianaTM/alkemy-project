create table if not exists cultura
(Cod_localidad int,
Id_provincia int,
Id_departamento int,
Categoría varchar (50),
Provincia varchar (50),
Localidad varchar (50),
Nombre varchar (60),
Domicilio varchar (50),
CP varchar (15),
Teléfono varchar (25),
Mail varchar(50),
Web varchar(50),
Fecha_carga date
);

create table if not exists Registros
(
Categoría varchar (50),
Provincia varchar (60),
Fuente varchar (50),
Total_por_categoría int,
Total_por_fuente int,
Total_categoría_por_provincia int,
Fecha_carga date
);

create table if not exists Salas_de_cine
(
Provincia varchar (50),
Pantallas int,
Butacas int,
espacio_INCAA int,
Fecha_carga date
);