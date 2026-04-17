import csv
import os

# Configuración de rutas
DATA_DIR = "data"
USUARIOS_CSV = os.path.join(DATA_DIR, "usuarios.csv")

def inicializar_usuarios():
    """Crea la base de datos de usuarios si no existe"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Usuario maestro por defecto (limpio de espacios)
            writer.writerow(["admin", "1234"])

def verificar_usuario(user, password):
    """
    Verifica credenciales eliminando espacios invisibles (.strip())
    tanto en lo que escribió el usuario como en lo que hay en el archivo.
    """
    if not os.path.exists(USUARIOS_CSV):
        inicializar_usuarios()
        return user.strip() == "admin" and password.strip() == "1234"
        
    with open(USUARIOS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for fila in reader:
            if len(fila) >= 2:
                # Limpiamos los datos del archivo y los ingresados para comparar
                u_archivo = fila[0].strip()
                p_archivo = fila[1].strip()
                u_ingresado = user.strip()
                p_ingresada = password.strip()
                
                if u_archivo == u_ingresado and p_archivo == p_ingresada:
                    return True
    return False

def registrar_usuario_csv(user, password):
    """Guarda un nuevo usuario limpiando espacios y asegurando nueva línea"""
    inicializar_usuarios()
    
    # Limpiamos antes de guardar para que el CSV nazca "limpio"
    u_limpio = user.strip()
    p_limpio = password.strip()
    
    with open(USUARIOS_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([u_limpio, p_limpio])

def guardar_movimiento_csv(fecha, concepto, monto, tipo, usuario):
    """Guarda el registro en el archivo personal del usuario"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # El nombre del archivo también se limpia de espacios por seguridad
    u_nombre = usuario.strip()
    nombre_archivo = f"gastos_{u_nombre}.csv"
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    
    file_exists = os.path.isfile(ruta)
    
    with open(ruta, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Fecha", "Concepto", "Monto", "Tipo"])
        
        # Guardamos el concepto también limpio de espacios extras
        writer.writerow([fecha, concepto.strip(), monto, tipo]) 

def modificar_password_csv(usuario, nueva_password):
    """Sobrescribe la contraseña del usuario en el archivo principal"""
    import csv
    import os
    
    ruta = os.path.join("data", "usuarios.csv")
    temp_data = []
    actualizado = False

    # 1. Leemos todo y modificamos en memoria
    with open(ruta, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for fila in reader:
            if len(fila) >= 2:
                if fila[0].strip() == usuario.strip():
                    temp_data.append([usuario.strip(), nueva_password.strip()])
                    actualizado = True
                else:
                    temp_data.append(fila)

    # 2. Volvemos a escribir el archivo con el cambio
    if actualizado:
        with open(ruta, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(temp_data)
        return True
    return False        