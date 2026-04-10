import customtkinter as ctk
from datetime import datetime

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zennit - Registro de Gasto")
        self.geometry("400x500")

        # --- Campo de Fecha (Automática) ---
        self.label_fecha = ctk.CTkLabel(self, text="Fecha:")
        self.label_fecha.pack(pady=(20, 0))
        
        # Obtenemos la fecha del sistema
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        
        self.entry_fecha = ctk.CTkEntry(self)
        self.entry_fecha.insert(0, fecha_actual) # Insertamos la fecha automática al inicio
        self.entry_fecha.pack(pady=5)

        # --- Campo de Concepto ---
        self.label_concepto = ctk.CTkLabel(self, text="Concepto (ej. Cena, Renta):")
        self.label_concepto.pack(pady=(10, 0))
        self.entry_concepto = ctk.CTkEntry(self, placeholder_text="¿En qué gastaste?")
        self.entry_concepto.pack(pady=5)

        # --- Campo de Monto ---
        self.label_monto = ctk.CTkLabel(self, text="Monto:")
        self.label_monto.pack(pady=(10, 0))
        self.entry_monto = ctk.CTkEntry(self, placeholder_text="0.00")
        self.entry_monto.pack(pady=5)

        # --- Botón Guardar ---
        self.boton_guardar = ctk.CTkButton(self, text="Guardar Gasto", command=self.guardar_datos)
        self.boton_guardar.pack(pady=30)

    def guardar_datos(self):
        # Aquí capturamos lo que hay en los cuadros de texto
        fecha = self.entry_fecha.get()
        concepto = self.entry_concepto.get()
        monto = self.entry_monto.get()
        
        print(f"Registrando: {fecha} | {concepto} | ${monto}")
        # El siguiente paso será enviar esto a logic.py