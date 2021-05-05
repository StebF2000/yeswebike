echo "Creem taula $1"


psql -U user bd -c "CREATE TABLE $1 (
    station_id smallint PRIMARY KEY,
    adress varchar(50),
    latitude int,
    longitude int,
    altitud int
    );"





