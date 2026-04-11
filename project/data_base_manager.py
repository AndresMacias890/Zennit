import csv
import os

# Ruta hacia la carpeta data que creamos al inicio
RUTA_ARCHIVO = "data/gastos.csv"

def guardar_movimiento_csv(fecha, concepto, monto):
    # Crear la carpeta data si no existe
    if not os.path.exists("data"):
        os.makedirs("data")
        
    archivo_existe = os.path.isfile(RUTA_ARCHIVO)
    
    with open(RUTA_ARCHIVO, mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        # Si el archivo es nuevo, añadimos los encabezados
        if not archivo_existe:
            escritor.writerow(["Fecha", "Concepto", "Monto"])
        
        escritor.writerow([fecha, concepto, monto])