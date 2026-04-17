import csv
import os

def validar_movimiento(monto_str, concepto):
    """Limpia espacios y valida que los datos sean correctos"""
    # Quitamos espacios al concepto
    concepto_limpio = concepto.strip()
    
    if not concepto_limpio:
        return False, "El concepto no puede estar vacío"
    
    try:
        # Quitamos espacios al monto por si acaso
        monto_f = float(monto_str.strip())
        if monto_f <= 0:
            return False, "El monto debe ser mayor a 0"
        return True, monto_f
    except ValueError:
        return False, "Monto no válido"

def obtener_resumen_finanzas(usuario):
    """Lee solo el archivo CSV del usuario actual"""
    # Limpiamos el nombre del usuario para buscar el archivo correcto
    nombre_archivo = f"gastos_{usuario.strip()}.csv"
    ruta = os.path.join("data", nombre_archivo)
    
    movimientos = []
    ingresos = 0
    gastos = 0
    
    if not os.path.exists(ruta):
        return movimientos, 0, 0, 0
        
    with open(ruta, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            # Limpiamos posibles espacios en los datos leídos
            monto = float(fila['Monto'])
            tipo = fila['Tipo'].strip()
            
            movimientos.append(fila)
            
            if tipo == "Ingreso":
                ingresos += monto
            else:
                gastos += monto
                
    balance = ingresos - gastos
    return movimientos, ingresos, gastos, balance

def formatear_con_puntos(numero_str):
    """Añade puntos de miles mientras el usuario escribe"""
    if not numero_str:
        return ""
    try:
        # Elimina cualquier cosa que no sea dígito por seguridad
        solo_numeros = "".join(filter(str.isdigit, numero_str))
        if not solo_numeros: return ""
        # Formatea con puntos: 1.000.000
        return "{:,}".format(int(solo_numeros)).replace(",", ".")
    except:
        return numero_str

def limpiar_formato_moneda(monto_formateado):
    """Quita los puntos para poder convertir a float"""
    return monto_formateado.replace(".", "").strip()