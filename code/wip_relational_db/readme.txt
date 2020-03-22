build_corona_db:
    Eingabe:
        DB-Name:        Name für die lokale Corona Datenbank
        User Name:      Postgres-User-Name; default: postgres
        Password:       Passwort für postgres
        Port:           Lokaler Port; default: 5432

add_to_corona_db:
    Eingabe:
        Add CSV:        Dateiname der csv im raw_data ordner
        Id Variable:    Id für Daten Join; default: Id wird aus colnames erraten
        DB-Name:        Name der lokalen Corona Datenbank
        User Name:      Postgres-User-Name; default: postgres
        Password:       Passwort für postgres
        Port:           Lokaler Port; default: 5432
    Für jede Spalte: 
        Bestätigung der Aufnahme in DB mit 'T'
        Data Type:      Datentyp der neuen Spalte


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