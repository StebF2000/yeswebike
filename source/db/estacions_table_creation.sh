echo "Creem taula $1"


sudo psql -U root webike -c "CREATE TABLE $1 (
    adress varchar(50),
    latitude float,
    longitude float,
    altitud int,
    station_id smallint PRIMARY KEY
      );"





