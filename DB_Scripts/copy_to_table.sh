echo "copiem el fitxer $1 a la taula $2"

psql -U user db -c "\COPY $2 FROM $1 DELIMITER ',';"
