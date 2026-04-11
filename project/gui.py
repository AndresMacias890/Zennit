import customtkinter as ctk
from datetime import datetime

# librerias que conectan con los otros archivos 
from project.logic import validar_movimiento, formatear_con_puntos, limpiar_formato_moneda
from project.data_base_manager import guardar_movimiento_csv

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- 1. AQUÍ DEFINES LA VARIABLE DE CONTROL ---
        # Debe estar después de super() y antes de usarla en el Entry
        self.monto_var = ctk.StringVar()
        
        # Aquí le dices que "vigile" los cambios y llame a la función de los puntos
        self.monto_var.trace_add("write", self.aplicar_mascara_monto)

        self.title("Zennit - Gestor Financiero")
        self.geometry("400x500")

        # ... (otros widgets como fecha y concepto) ...

        # --- 2. AQUÍ LA CONECTAS AL ENTRY ---
        self.label_monto = ctk.CTkLabel(self, text="Monto:")
        self.label_monto.pack(pady=(10, 0))
        
        # Es CRUCIAL que uses 'textvariable=self.monto_var'
        self.entry_monto = ctk.CTkEntry(
            self, 
            textvariable=self.monto_var, 
            placeholder_text="0"
        )
        self.entry_monto.pack(pady=5)

    # --- LAS FUNCIONES VAN FUERA DEL __init__ PERO DENTRO DE LA CLASE ---
    def aplicar_mascara_monto(self, *args):
        # ... (código de los puntos) ...

        # --- Título ---
        self.label_titulo = ctk.CTkLabel(self, text="Nuevo Movimiento", font=("Arial", 20))
        self.label_titulo.pack(pady=20)

        # --- Campo de Fecha ---
        self.label_fecha = ctk.CTkLabel(self, text="Fecha:")
        self.label_fecha.pack(pady=(10, 0))
        self.entry_fecha = ctk.CTkEntry(self)
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_fecha.pack(pady=5)

        # --- Campo de Concepto ---
        self.label_concepto = ctk.CTkLabel(self, text="Concepto:")
        self.label_concepto.pack(pady=(10, 0))
        self.entry_concepto = ctk.CTkEntry(self, placeholder_text="Ej: Supermercado")
        self.entry_concepto.pack(pady=5)

        # --- Campo de Monto ---
        self.label_monto = ctk.CTkLabel(self, text="Monto:")
        self.label_monto.pack(pady=(10, 0))
        self.entry_monto = ctk.CTkEntry(self, placeholder_text="0.00")
        self.entry_monto.pack(pady=5)

        # --- Botón Guardar ---
        self.boton_guardar = ctk.CTkButton(self, text="Guardar Gasto", command=self.guardar_datos)
        self.boton_guardar.pack(pady=30)

def aplicar_mascara_monto(self, *args):
        texto_actual = self.monto_var.get()
        
        # Filtramos para que solo pasen números
        solo_numeros = "".join(filter(str.isdigit, texto_actual))
        
        # Aplicamos los puntos de miles usando la función de logic.py
        formateado = formatear_con_puntos(solo_numeros)
        
        # Solo actualizamos si el texto cambió (para evitar bucles infinitos)
        if texto_actual != formateado:
            self.monto_var.set(formateado)

def guardar_datos(self):
        fecha = self.entry_fecha.get()
        concepto = self.entry_concepto.get()
        
        # LIMPIAMOS los puntos antes de procesar
        monto_con_puntos = self.monto_var.get()
        monto_limpio = limpiar_formato_moneda(monto_con_puntos)
        
        es_valido, resultado = validar_movimiento(monto_limpio, concepto)
        
        if es_valido:
            guardar_movimiento_csv(fecha, concepto, resultado)
            print(f"✅ Guardado: {concepto} - ${resultado}")
            # Limpiamos los campos
            self.monto_var.set("") 
            self.entry_concepto.delete(0, 'end')
        else:
            print(f"❌ Error: {resultado}")

if __name__ == "__main__":
    app = App()
    app.mainloop()       