echo "Creem taula $1"


sudo psql -U root webike -c "CREATE TABLE $1 (
    station_id smallint,
    num_bikes smallint,
    num_bikes_mech smallint,
    num_bikes_ebike smallint,
    num_docks_free smallint,
    datestamp int,
    is_changing bool,
    status varchar(10),
    is_installed bool,
    is_renting bool,
    is_returning bool,
    ttl smallint
    );"





