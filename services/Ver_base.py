from db import databas

crsr = databas.cursor()
valores = "Asalto"
crsr.execute("SELECT * FROM Hilo")
print(crsr.fetchall())