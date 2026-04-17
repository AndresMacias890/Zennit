import customtkinter as ctk
from datetime import datetime
from tkcalendar import Calendar

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
    registrar_usuario_csv,
    modificar_password_csv
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
        
        # --- MENÚ LATERAL
        self.menu_lateral = ctk.CTkFrame(self.main_container, width=220, corner_radius=0)
        self.menu_lateral.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.menu_lateral, text="ZENNIT PRO", font=("Arial", 20, "bold")).pack(pady=25)
        ctk.CTkLabel(self.menu_lateral, text=f"Hola, {usuario}", font=("Arial", 14)).pack(pady=(0, 20))

        # Botón Panel Principal (Ahora con el comando corregido)
        ctk.CTkButton(self.menu_lateral, text="📊 Panel Principal", fg_color="#2b719e", anchor="w", command=self.dibujar_elementos_panel).pack(fill="x", padx=15, pady=5)

        # Botón Calendario
        ctk.CTkButton(self.menu_lateral, text="📅 Calendario", fg_color="transparent", anchor="w", command=self.mostrar_calendario).pack(fill="x", padx=15, pady=5)

        # Botón Ajustes
        ctk.CTkButton(self.menu_lateral, text="⚙️ Ajustes y Perfil", fg_color="transparent", anchor="w", command=self.mostrar_ajustes_perfil).pack(fill="x", padx=15, pady=5)

        # Botón Cerrar Sesión
        ctk.CTkButton(self.menu_lateral, text="🚪 Cerrar Sesión", fg_color="#444", command=self.mostrar_login).pack(side="bottom", pady=25, padx=15)
        
        
        # Área Principal
        self.area_principal = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.area_principal.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.dibujar_elementos_panel()

    def dibujar_elementos_panel(self):
        
        
        for widget in self.area_principal.winfo_children():
            widget.destroy()
       
       
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
    
    def mostrar_ajustes_perfil(self):
        """Pantalla para gestionar el perfil y la apariencia"""
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        # Título
        ctk.CTkLabel(self.area_principal, text="Configuración de Perfil", font=("Arial", 24, "bold")).pack(pady=20)

        # --- SECCIÓN PERFIL ---
        frame_perfil = ctk.CTkFrame(self.area_principal)
        frame_perfil.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(frame_perfil, text="Información de Usuario", font=("Arial", 16, "bold")).pack(pady=10, padx=20, anchor="w")
        ctk.CTkLabel(frame_perfil, text=f"Nombre de usuario: {self.usuario_actual}").pack(pady=5, padx=20, anchor="w")
        
        # --- SECCIÓN SEGURIDAD ---
        frame_pass = ctk.CTkFrame(self.area_principal)
        frame_pass.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(frame_pass, text="Cambiar Contraseña", font=("Arial", 16, "bold")).pack(pady=10, padx=20, anchor="w")
        
        self.entry_nueva_pass = ctk.CTkEntry(frame_pass, placeholder_text="Nueva contraseña", show="*", width=200)
        self.entry_nueva_pass.pack(side="left", padx=20, pady=20)
        
        ctk.CTkButton(frame_pass, text="Actualizar Clave", width=120, command=self.actualizar_password).pack(side="left", padx=10)

        # --- SECCIÓN APARIENCIA ---
        frame_tema = ctk.CTkFrame(self.area_principal)
        frame_tema.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(frame_tema, text="Apariencia", font=("Arial", 16, "bold")).pack(pady=10, padx=20, anchor="w")
        
        self.tema_var = ctk.StringVar(value="Oscuro")
        ctk.CTkOptionMenu(frame_tema, values=["System", "Light", "Dark"], 
                          command=self.cambiar_apariencia).pack(pady=10, padx=20, anchor="w")

        self.label_feedback_ajustes = ctk.CTkLabel(self.area_principal, text="")
        self.label_feedback_ajustes.pack(pady=20)

    def cambiar_apariencia(self, nuevo_tema):
        """Cambia el modo de color de la app al vuelo"""
        ctk.set_appearance_mode(nuevo_tema)

    def actualizar_password(self):
        """Lógica para cambiar la clave del usuario actual"""
        nueva_p = self.entry_nueva_pass.get().strip()
        if nueva_p:
            # Aquí llamaremos a una función del data_base_manager
            exito = modificar_password_csv(self.usuario_actual, nueva_p)
            if exito:
                self.label_feedback_ajustes.configure(text="✅ Contraseña actualizada", text_color="#2FA572")
                self.entry_nueva_pass.delete(0, 'end')
            else:
                self.label_feedback_ajustes.configure(text="❌ Error al actualizar", text_color="#eb5e5e")
        else:
            self.label_feedback_ajustes.configure(text="⚠ Escribe una contraseña válida", text_color="#eb5e5e")
    
    def mostrar_calendario(self):
        """Pantalla con calendario para ver gastos por día"""
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.area_principal, text="Agenda Financiera", font=("Arial", 24, "bold")).pack(pady=20)

        # Contenedor para el calendario
        frame_cal = ctk.CTkFrame(self.area_principal)
        frame_cal.pack(pady=10, padx=20, fill="both", expand=True)

        # Configuramos el calendario
        # locale='es_ES' lo pone en español, date_pattern define el formato de fecha
        self.cal = Calendar(frame_cal, selectmode='day', 
                           locale='es_ES', date_pattern='dd/mm/yyyy',
                           background="#2b719e", foreground="white", 
                           selectbackground="#2FA572")
        self.cal.pack(pady=20, padx=20)

        ctk.CTkButton(frame_cal, text="Consultar este día", 
                      command=self.consultar_gastos_fecha, width=200).pack(pady=10)

        # ScrollableFrame para mostrar los resultados del día sin amontonar
        self.frame_resumen_cal = ctk.CTkScrollableFrame(frame_cal, label_text="Detalle del día", height=200)
        self.frame_resumen_cal.pack(fill="x", padx=40, pady=20)

    def consultar_gastos_fecha(self):
        """Busca movimientos en el archivo del usuario que coincidan con la fecha del calendario"""
        fecha_sel = self.cal.get_date()
        
        # Limpiamos el frame de resultados anterior
        for widget in self.frame_resumen_cal.winfo_children():
            widget.destroy()
            
        # Obtenemos los datos del usuario actual
        movs, _, _, _ = obtener_resumen_finanzas(self.usuario_actual)
        
        # Filtramos por fecha seleccionada
        gastos_dia = [m for m in movs if m['Fecha'] == fecha_sel]
        
        if gastos_dia:
            total_neto = 0
            for g in gastos_dia:
                es_ingreso = g['Tipo'] == "Ingreso"
                color = "#2FA572" if es_ingreso else "#eb5e5e"
                simbolo = "+" if es_ingreso else "-"
                monto = float(g['Monto'])
                
                texto_gasto = f"• {g['Concepto']}: {simbolo}${monto:,.2f}"
                ctk.CTkLabel(self.frame_resumen_cal, text=texto_gasto, text_color=color).pack(anchor="w")
                
                total_neto += monto if es_ingreso else -monto
            
            # Mostrar balance final del día
            color_balance = "#2FA572" if total_neto >= 0 else "#eb5e5e"
            ctk.CTkLabel(self.frame_resumen_cal, text=f"\nBalance del día: ${total_neto:,.2f}", 
                         font=("Arial", 14, "bold"), text_color=color_balance).pack(pady=5)
        else:
            ctk.CTkLabel(self.frame_resumen_cal, text=f"No hay registros para el {fecha_sel}", 
                         text_color="gray").pack(pady=10)                         