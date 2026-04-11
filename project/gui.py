import customtkinter as ctk
from datetime import datetime
from project.logic import validar_movimiento, formatear_con_puntos, limpiar_formato_moneda
from project.data_base_manager import guardar_movimiento_csv

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración de la ventana
        self.title("Zennit - Gestor Financiero")
        self.geometry("400x550")

        # 2. Variable de control para el monto
        self.monto_var = ctk.StringVar()
        self.monto_var.trace_add("write", self.aplicar_mascara_monto)

        # --- Interfaz ---
        ctk.CTkLabel(self, text="Nuevo Movimiento", font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkLabel(self, text="Fecha:").pack(pady=(10, 0))
        self.entry_fecha = ctk.CTkEntry(self)
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_fecha.pack(pady=5)

        ctk.CTkLabel(self, text="Concepto:").pack(pady=(10, 0))
        self.entry_concepto = ctk.CTkEntry(self, placeholder_text="Ej: Supermercado")
        self.entry_concepto.pack(pady=5)

        ctk.CTkLabel(self, text="Monto:").pack(pady=(10, 0))
        self.entry_monto = ctk.CTkEntry(self, textvariable=self.monto_var, placeholder_text="0")
        self.entry_monto.pack(pady=5)

        # El botón DEBE llamar a self.guardar_datos
        self.boton_guardar = ctk.CTkButton(self, text="Guardar Gasto", command=self.guardar_datos)
        self.boton_guardar.pack(pady=30)

    # --- MÉTODOS DE LA CLASE (Deben tener 4 espacios de sangría) ---

    def aplicar_mascara_monto(self, *args):
        texto = self.monto_var.get()
        solo_numeros = "".join(filter(str.isdigit, texto))
        formateado = formatear_con_puntos(solo_numeros)
        if texto != formateado:
            self.monto_var.set(formateado)

    def guardar_datos(self):
        fecha = self.entry_fecha.get()
        concepto = self.entry_concepto.get()
        monto_sucio = self.monto_var.get()
        
        monto_limpio = limpiar_formato_moneda(monto_sucio)
        es_valido, resultado = validar_movimiento(monto_limpio, concepto)
        
        if es_valido:
            guardar_movimiento_csv(fecha, concepto, resultado)
            print(f"✅ ¡Éxito! Guardado {concepto}")
            # Limpiar campos
            self.monto_var.set("")
            self.entry_concepto.delete(0, 'end')
        else:
            print(f"❌ Error: {resultado}")

if __name__ == "__main__":
    app = App()
    app.mainloop()       