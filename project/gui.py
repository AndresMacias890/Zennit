import customtkinter as ctk
from datetime import datetime

# librerias que conectan con los otros archivos 
from project.logic import validar_movimiento
from project.data_base_manager import guardar_movimiento_csv

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Zennit - Gestor Financiero")
        self.geometry("400x500")

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

    def guardar_datos(self):
        # 1. Obtener datos de los cuadritos de texto
        fecha = self.entry_fecha.get()
        concepto = self.entry_concepto.get()
        monto = self.entry_monto.get()
        
        # 2. Validar con la función de logic.py
        es_valido, resultado = validar_movimiento(monto, concepto)
        
        if es_valido:
            # 3. Guardar con la función de data_base_manager.py
            guardar_movimiento_csv(fecha, concepto, resultado)
            
            print(f"✅ Guardado con éxito: {concepto} por ${resultado}")
            
            # Limpiar para el siguiente ingreso
            self.entry_concepto.delete(0, 'end')
            self.entry_monto.delete(0, 'end')
        else:
            # Mostrar error en la consola por ahora
            print(f"❌ Error de validación: {resultado}")

if __name__ == "__main__":
    app = App()
    app.mainloop()       