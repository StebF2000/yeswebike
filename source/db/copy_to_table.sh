echo "copiem el fitxer $1 a la taula $2"

sudo psql -U root webike -c "\COPY $2 FROM $1 DELIMITER ',';"
