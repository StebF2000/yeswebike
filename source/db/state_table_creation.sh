echo "Creem taula $1"


sudo psql -U root webike -c "CREATE TABLE $1 (
    capacity smallint,
    available_bikes smallint,
    mechanical_bikes smallint,
    electric_bikes smallint,
    free_docks smallint,
    charging bool,
    status char(5),
    installed bool,
    rending bool,
    returning bool,
    station_id smallint PRIMARY KEY
      );"


