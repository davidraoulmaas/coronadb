build_corona_db:
    Eingabe:
        DB-Name:        Name für die lokale Corona Datenbank
        User Name:      Postgres-User-Name; default: postgres
        Password:       Passwort für postgres
        Port:           Lokaler Port; default: 5432

add_to_corona_db [files] [--auto-detect]:
	files:		Eine oder mehrere CSVs aus dem raw-data-Ordner
	--auto-detect	Aktiviert automatische Erkennung des geogr. Levels  
    Eingabe:
        DB-Name:        Name der lokalen Corona Datenbank
        User Name:      Postgres-User-Name; default: postgres
        Password:       Passwort für postgres
        Port:           Lokaler Port; default: 5432
    Für jede Spalte: 
        Bestätigung der Aufnahme in DB mit 'T'
        Data Type:      Datentyp der neuen Spalte

update_corona_cases:
    Eingabe:
        DB-Name:        Name der lokalen Corona Datenbank
        User Name:      Postgres-User-Name; default: postgres
        Password:       Passwort für postgres
        Port:           Lokaler Port; default: 5432


DB Schema:
    land(land)
    kreis(krs, land -> land.land)
    distrikt(plz, krs -> kreis.krs)
    fälle(krs -> kreis.krs)

SQL-Integration funktionsfähig für Datensätze:
- bev.csv
- intensiv.csv
- krankenh.csv
- numhochschulen_per_plz.csv
- pflegebed.csv

TO GO:
Integration der anderen Datensätze
Update Routinen für Datensätze + Corona-Fallzahlen