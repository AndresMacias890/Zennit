import os
import sys

# Detectamos la ruta de tu usuario con espacios correctamente
appdata = os.environ.get('LOCALAPPDATA')

# Construimos las rutas usando comillas dobles internas por seguridad
tcl_path = os.path.join(appdata, "Programs", "Python", "Python313", "tcl", "tcl8.6")
tk_path = os.path.join(appdata, "Programs", "Python", "Python313", "tcl", "tk8.6")

# Inyectamos las rutas al sistema antes de importar cualquier cosa gráfica
os.environ['TCL_LIBRARY'] = tcl_path
os.environ['TK_LIBRARY'] = tk_path

from project.helper import obtener_post
from project.gui import App 

# Esto obtiene los datos
post = obtener_post()
print("Primeros 5 posts: ")
for p in post[:5]:
    print(f"ID:{p['id']} - Titulo:{p['title']}")

# Esto lanza la interfaz gráfica
if __name__ == "__main__":
    app = App()
    app.mainloop()