# register_gui.py
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
from PIL import Image, ImageTk
import user_management as um  # Asegúrate de que el archivo user_management.py esté configurado correctamente

class RegisterApp:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app  # Guarda la instancia de la ventana de login
        self.root.title("Registro de Usuario - Sistema de Detección Dental")
        self.root.geometry("400x800")  # Tamaño ajustado
        self.root.resizable(False, False)
        
        # Instancia de UserManager para manejar usuarios
        try:
            self.user_manager = um.UserManager()
            print("Conexión a UserManager creada exitosamente.")
        except Exception as e:
            print(f"Error al crear UserManager: {e}")
            Messagebox.show_error("Error", "No se pudo establecer conexión con la base de datos.")
            return

        # Centrar la ventana
        self.center_window(400, 800)

        # Cargar íconos
        self.register_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen27.png").resize((30, 30)))
        self.login_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen26.png").resize((30, 30)))
        
        # Crear el marco del formulario
        self.form_frame = ttk.LabelFrame(root, text="Formulario de Registro", padding=15, bootstyle="info")
        self.form_frame.pack(pady=10, fill="x", expand=True)

        # Campos de entrada
        ttk.Label(self.form_frame, text="Nombres", font=("Arial", 12)).pack(pady=5)
        self.nombres_entry = ttk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.nombres_entry.pack(pady=5)

        ttk.Label(self.form_frame, text="Apellidos", font=("Arial", 12)).pack(pady=5)
        self.apellidos_entry = ttk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.apellidos_entry.pack(pady=5)

        ttk.Label(self.form_frame, text="Correo Electrónico", font=("Arial", 12)).pack(pady=5)
        self.correo_entry = ttk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.correo_entry.pack(pady=5)

        ttk.Label(self.form_frame, text="Número de Teléfono", font=("Arial", 12)).pack(pady=5)
        self.telefono_entry = ttk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.telefono_entry.pack(pady=5)

        # Selector de Fecha de Nacimiento
        ttk.Label(self.form_frame, text="Fecha de Nacimiento", font=("Arial", 12)).pack(pady=5)
        self.create_date_selector(self.form_frame)

        # Contraseña
        ttk.Label(self.form_frame, text="Contraseña", font=("Arial", 12)).pack(pady=5)
        self.contrasena_entry = ttk.Entry(self.form_frame, show="*", font=("Arial", 12), width=30)
        self.contrasena_entry.pack(pady=5)

        # Menú de selección de rol
        roles = ["Seleccionar", "Administrador", "Odontólogo", "Paciente"]
        self.rol_seleccionado = ttk.StringVar(value=roles[0])
        ttk.Label(self.form_frame, text="Rol", font=("Arial", 12)).pack(pady=5)
        self.menu_rol = ttk.OptionMenu(self.form_frame, self.rol_seleccionado, *roles)
        self.menu_rol.pack(pady=5)

        # Botón para registrar
        self.boton_registro = ttk.Button(
            root, 
            text=" Registrarse", 
            image=self.register_icon, 
            compound="left", 
            command=self.registrar, 
            bootstyle="outline-success", 
            width=20
        )
        self.boton_registro.pack(pady=15)

        # Botón para regresar al login
        self.boton_iniciar_sesion = ttk.Button(
            root, 
            text=" Iniciar Sesión", 
            image=self.login_icon, 
            compound="left", 
            command=self.volver_a_login, 
            bootstyle="outline-info", 
            width=20
        )
        self.boton_iniciar_sesion.pack(pady=10)

    def center_window(self, width, height):
        """Centrar la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_date_selector(self, parent):
        """Crear selector de fecha de nacimiento."""
        frame = ttk.Frame(parent)
        frame.pack(pady=5)

        days = list(range(1, 32))
        self.dia_combobox = ttk.Combobox(frame, values=days, width=5, font=("Arial", 12))
        self.dia_combobox.set("Día")
        self.dia_combobox.grid(row=0, column=0, padx=5)

        months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        self.mes_combobox = ttk.Combobox(frame, values=months, width=5, font=("Arial", 12))
        self.mes_combobox.set("Mes")
        self.mes_combobox.grid(row=0, column=1, padx=5)

        current_year = datetime.now().year
        years = list(range(current_year - 100, current_year + 1))
        self.anio_combobox = ttk.Combobox(frame, values=years, width=8, font=("Arial", 12))
        self.anio_combobox.set("Año")
        self.anio_combobox.grid(row=0, column=2, padx=5)

    def obtener_fecha_nacimiento(self):
        """Obtener fecha de nacimiento en formato datetime.date."""
        try:
            dia = int(self.dia_combobox.get())
            mes = self.mes_combobox.get()
            anio = int(self.anio_combobox.get())
            numero_mes = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"].index(mes) + 1
            return datetime(anio, numero_mes, dia).date()
        except ValueError:
            print("Error al obtener la fecha de nacimiento")
            return None

    def volver_a_login(self):
        """Cerrar la ventana de registro y volver al login"""
        self.root.destroy()  # Cierra la ventana de registro
        if self.login_app:
            self.login_app.root.deiconify()  # Muestra la ventana de login

    def registrar(self):
        """Registrar el usuario en la base de datos."""
        print("Intentando registrar el usuario...")
        nombres = self.nombres_entry.get().strip()
        apellidos = self.apellidos_entry.get().strip()
        correo = self.correo_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        fecha_nacimiento = self.obtener_fecha_nacimiento()
        contrasena = self.contrasena_entry.get().strip()
        rol = self.rol_seleccionado.get()

        # Validación de campos
        if not (nombres and apellidos and correo and telefono and fecha_nacimiento and contrasena and rol != "Seleccionar"):
            print("Campos incompletos detectados.")
            Messagebox.show_warning("Advertencia", "Por favor, complete todos los campos.")
            return
        
        try:
            resultado = self.user_manager.agregar_usuario(nombres, apellidos, correo, telefono, fecha_nacimiento, contrasena, rol)
            print(f"Resultado de agregar usuario: {resultado}")
            
            if resultado == "DUPLICADO":
                Messagebox.show_warning("Advertencia", "El correo ya está registrado. Intente con otro.")
            elif resultado == "REGISTRADO":
                Messagebox.show_info("Registro Exitoso", "Usuario registrado con éxito")
                self.root.destroy()  # Cierra la ventana de registro después del registro exitoso
                if self.login_app:
                    self.login_app.root.deiconify()  # Vuelve a mostrar la ventana de login
            else:
                Messagebox.show_error("Error", "Ocurrió un problema al registrar el usuario.")
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            Messagebox.show_error("Error", "Ocurrió un problema inesperado. Intente de nuevo.")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = RegisterApp(root, None)  # None aquí ya que no hay ventana de login en modo prueba
    root.mainloop()
