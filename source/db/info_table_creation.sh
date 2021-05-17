echo "Creem taula $1"


sudo psql -U root webike -c "CREATE TABLE $1 (
    station_id smallint,
    capacity smallint,
    last_updated timestamp
    );"





