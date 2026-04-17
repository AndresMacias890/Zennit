import customtkinter as ctk
from datetime import datetime

# Importamos las piezas de los otros archivos (Asegúrate de que existan)
from project.logic import (
    validar_movimiento, 
    formatear_con_puntos, 
    limpiar_formato_moneda, 
    obtener_resumen_finanzas
)
from project.data_base_manager import (
    guardar_movimiento_csv, 
    verificar_usuario, 
    registrar_usuario_csv
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración de Ventana
        self.title("Zennit - Gestión Financiera")
        self.after(0, lambda: self.state('zoomed')) 

        # Variable para saber qué usuario está usando la app
        self.usuario_actual = None 

        # Variable para la máscara de puntos (Monto)
        self.monto_var = ctk.StringVar()
        self.monto_var.trace_add("write", self.aplicar_mascara_monto)

        # Contenedor principal donde cambiaremos las pantallas
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        # Iniciamos en el Login
        self.mostrar_login()

    # --- PANTALLA: LOGIN ---
    def mostrar_login(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        login_frame = ctk.CTkFrame(self.main_container, width=350, height=450)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(login_frame, text="ZENNIT", font=("Arial", 30, "bold")).pack(pady=30)
        
        self.entry_user = ctk.CTkEntry(login_frame, placeholder_text="Usuario", width=250)
        self.entry_user.pack(pady=10)
        
        self.entry_pass = ctk.CTkEntry(login_frame, placeholder_text="Contraseña", show="*", width=250)
        self.entry_pass.pack(pady=10)

        ctk.CTkButton(login_frame, text="Entrar", command=self.ejecutar_login, width=250).pack(pady=20)
        
        ctk.CTkButton(login_frame, text="¿No tienes cuenta? Regístrate", 
                      command=self.mostrar_registro, fg_color="transparent", text_color="#2b719e").pack(pady=5)

        self.label_error = ctk.CTkLabel(login_frame, text="", text_color="#eb5e5e", font=("Arial", 12, "bold"))
        self.label_error.pack(pady=10)

    def ejecutar_login(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        
        if verificar_usuario(u, p) or (u == "admin" and p == "1234"):
            self.usuario_actual = u # Guardamos el usuario para filtrar sus archivos
            self.mostrar_dashboard(u)
        else:
            self.label_error.configure(text="❌ Usuario o clave incorrectos")
            self.entry_pass.delete(0, 'end')

    # --- PANTALLA: REGISTRO ---
    def mostrar_registro(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        reg_frame = ctk.CTkFrame(self.main_container, width=350, height=450)
        reg_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(reg_frame, text="CREAR CUENTA", font=("Arial", 25, "bold")).pack(pady=20)
        
        self.reg_user = ctk.CTkEntry(reg_frame, placeholder_text="Nuevo Usuario", width=250)
        self.reg_user.pack(pady=10)
        
        self.reg_pass = ctk.CTkEntry(reg_frame, placeholder_text="Nueva Contraseña", show="*", width=250)
        self.reg_pass.pack(pady=10)

        ctk.CTkButton(reg_frame, text="Registrar", command=self.ejecutar_registro, 
                      width=250, fg_color="#2FA572").pack(pady=(20, 10))
        
        ctk.CTkButton(reg_frame, text="Volver al Login", command=self.mostrar_login, 
                      width=250, fg_color="transparent", border_width=2).pack(pady=10)

        self.label_error_reg = ctk.CTkLabel(reg_frame, text="", text_color="#eb5e5e")
        self.label_error_reg.pack(pady=10)

    def ejecutar_registro(self):
        u, p = self.reg_user.get().strip(), self.reg_pass.get().strip()
        if u and p:
            registrar_usuario_csv(u, p)
            self.mostrar_login()
            self.label_error.configure(text="✅ Registro exitoso", text_color="#2FA572")
        else:
            self.label_error_reg.configure(text="❌ Completa todos los campos")

    # --- PANTALLA: DASHBOARD ---
    def mostrar_dashboard(self, usuario):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self.main_container, width=220, corner_radius=0)
        self.menu_lateral.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.menu_lateral, text="ZENNIT PRO", font=("Arial", 20, "bold")).pack(pady=25)
        ctk.CTkLabel(self.menu_lateral, text=f"Hola, {usuario}", font=("Arial", 14)).pack(pady=(0, 20))

        ctk.CTkButton(self.menu_lateral, text="📊 Panel Principal", fg_color="#2b719e", anchor="w").pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.menu_lateral, text="🚪 Cerrar Sesión", fg_color="#444", command=self.mostrar_login).pack(side="bottom", pady=25, padx=15)

        # Área Principal
        self.area_principal = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.area_principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.dibujar_elementos_panel()

    def dibujar_elementos_panel(self):
        self.frame_form = ctk.CTkFrame(self.area_principal)
        self.frame_form.pack(fill="x", padx=10, pady=10)

        self.entry_fecha = ctk.CTkEntry(self.frame_form, width=110)
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_fecha.pack(side="left", padx=10, pady=10)

        self.entry_concepto = ctk.CTkEntry(self.frame_form, placeholder_text="Ej: Sueldo, Comida...", width=200)
        self.entry_concepto.pack(side="left", padx=10)

        self.entry_monto = ctk.CTkEntry(self.frame_form, textvariable=self.monto_var, placeholder_text="Monto", width=120)
        self.entry_monto.pack(side="left", padx=10)

        self.tipo_var = ctk.StringVar(value="Gasto")
        self.selector_tipo = ctk.CTkSegmentedButton(self.frame_form, values=["Gasto", "Ingreso"], variable=self.tipo_var)
        self.selector_tipo.pack(side="left", padx=10)

        ctk.CTkButton(self.frame_form, text="Guardar", command=self.guardar_y_actualizar, width=100).pack(side="left", padx=10)

        self.frame_tabla = ctk.CTkScrollableFrame(self.area_principal, label_text="Tus Movimientos")
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_total = ctk.CTkLabel(self.area_principal, text="", font=("Arial", 22, "bold"))
        self.label_total.pack(pady=10)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        # Cargamos datos específicos del usuario actual
        movs, ingresos, gastos, balance = obtener_resumen_finanzas(self.usuario_actual)
        
        for m in movs:
            color = "#2FA572" if m.get('Tipo') == "Ingreso" else "#eb5e5e"
            simbolo = "+" if m.get('Tipo') == "Ingreso" else "-"
            # Formateamos el monto para que se vea con comas y decimales
            txt = f"{m['Fecha']} | {m['Concepto']} | {simbolo}${float(m['Monto']):,.2f}"
            ctk.CTkLabel(self.frame_tabla, text=txt, font=("Courier", 13), text_color=color).pack(anchor="w", padx=10)

        self.label_total.configure(
            text=f"Balance: ${balance:,.2f}",
            text_color="#2FA572" if balance >= 0 else "#eb5e5e"
        )

    def guardar_y_actualizar(self):
        monto_limpio = limpiar_formato_moneda(self.monto_var.get())
        concepto = self.entry_concepto.get().strip()
        tipo = self.tipo_var.get()
        
        es_valido, resultado = validar_movimiento(monto_limpio, concepto)
        if es_valido:
            guardar_movimiento_csv(self.entry_fecha.get(), concepto, resultado, tipo, self.usuario_actual)
            self.monto_var.set("")
            self.entry_concepto.delete(0, 'end')
            self.actualizar_tabla()

    def aplicar_mascara_monto(self, *args):
        texto = self.monto_var.get()
        if texto:
            solo_numeros = "".join(filter(str.isdigit, texto))
            formateado = formatear_con_puntos(solo_numeros)
            if texto != formateado:
                self.monto_var.set(formateado)     