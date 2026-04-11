# project/logic.py

def validar_movimiento(monto, concepto):
    """
    Verifica que el monto sea un número válido y que el concepto no esté vacío.
    Retorna (True, monto_float) si es válido, o (False, mensaje_error) si no.
    """
    if not concepto.strip():
        return False, "El concepto no puede estar vacío."

    try:
        monto_limpio = float(monto.replace(",", ".")) 
        if monto_limpio <= 0:
            return False, "El monto debe ser mayor a cero."
        return True, monto_limpio
    except ValueError:
        return False, "El monto debe ser un número válido."

def calcular_balance(lista_movimientos):
    # Aquí suma todos los montos 
    return sum(movimiento['monto'] for movimiento in lista_movimientos)

def limpiar_formato_moneda(texto_con_puntos):
    """Convierte '1.250,50' o '1.250' en un float de Python"""
    # Quitamos los puntos de miles
    limpio = texto_con_puntos.replace(".", "")
    # Cambiamos la coma decimal por punto si existiera
    limpio = limpio.replace(",", ".")
    return limpio

def formatear_con_puntos(valor):
    """Convierte un string numérico en uno con puntos de miles"""
    try:
        # Quitamos cualquier cosa que no sea número para evitar errores
        solo_numeros = "".join(filter(str.isdigit, valor))
        if not solo_numeros:
            return ""
        # Formateamos con puntos de miles: 1000 -> 1.000
        return f"{int(solo_numeros):,}".replace(",", ".")
    except:
        return valor