#!/bin/bash

psql -U admin postgres -c "CREATE TABLE informacio (
    id_estacio smallint,
    capacity smallint,
    pk varchar(25) PRIMARY KEY,
    last_updated int
    );"

echo "Taula informacio creada"

psql -U admin postgres -c "CREATE TABLE estacions (
	carrer varchar(50),
	latitud float,
	longitud float,
	altitud smallint,
	id_estacio smallint
	);"

echo "Taula estacions creada"

psql -U admin postgres -c "CREATE TABLE estat (
	id_estacio smallint,
	num_bikes_available smallint,
	num_bikes_avaliable_mechanical smallint,
	num_bikes_available_ebike smallint,
	num_docks_available smallint,
	is_installed bool,
	is_renting bool,
	is_returning bool,
	is_charching_station bool,
	status varchar(20),
	last_updated int,
	PK varchar(30)
	);"

echo "Taula estat creada"

psql -U admin postgres -c "\COPY estat FROM 'data/Estat.csv' DELIMITER ',';"
echo "Informació insertada correctament a la taula estat"

psql -U admin postgres -c "\COPY estacions FROM 'data/Estacions.csv' DELIMITER ',';"
echo "Informació insertada correctament a la taula estacons"

psql -U admin postgres -c "\COPY informacio FROM 'data/Informacio.csv' DELIMITER ',';"
echo "Informació insertada correctament a la taula informacio"
