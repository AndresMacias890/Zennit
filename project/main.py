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