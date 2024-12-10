# login_gui.py
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import user_management as um
import registerpac_gui as registerpac  # Importar el módulo para la gestión de pacientes
import register_gui
from registerpac_gui import PatientManagementApp
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión - Sistema de Detección Dental")
        self.root.geometry("500x600")
        self.user_manager = um.UserManager()
        
        self.style = Style(theme="superhero")
        self.center_window(500, 600)
        
        # Cargar imágenes
        self.logo_img = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen17.png").resize((200, 200)))
        self.user_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen23.png").resize((30, 30)))
        self.pass_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen20.png").resize((30, 30)))
        self.login_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen26.png").resize((30, 30)))
        self.register_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen27.png").resize((30, 30)))
        
        # Imagen de logo
        self.logo_label = ttk.Label(root, image=self.logo_img)
        self.logo_label.pack(pady=30)

        # Campo de entrada de correo electrónico con ícono
        frame_correo = ttk.Frame(root)
        frame_correo.pack(pady=15)
        correo_canvas = ttk.Canvas(frame_correo, width=300, height=40)
        correo_canvas.pack()
        correo_canvas.create_image(15, 20, image=self.user_icon, anchor="w")
        self.correo_entry = ttk.Entry(frame_correo, font=("Arial", 12), width=28)
        correo_canvas.create_window(55, 20, anchor="w", window=self.correo_entry)

        # Campo de entrada de contraseña con ícono
        frame_contrasena = ttk.Frame(root)
        frame_contrasena.pack(pady=15)
        contrasena_canvas = ttk.Canvas(frame_contrasena, width=300, height=40)
        contrasena_canvas.pack()
        contrasena_canvas.create_image(15, 20, image=self.pass_icon, anchor="w")
        self.contrasena_entry = ttk.Entry(frame_contrasena, show="*", font=("Arial", 12), width=28)
        contrasena_canvas.create_window(55, 20, anchor="w", window=self.contrasena_entry)

        # Botones
        self.boton_login = ttk.Button(root, text=" Iniciar Sesión", image=self.login_icon, compound="left", command=self.iniciar_sesion, bootstyle="outline-success", width=20)
        self.boton_login.pack(pady=20)
        self.boton_registro = ttk.Button(root, text=" Registrarse", image=self.register_icon, compound="left", command=self.abrir_registro, bootstyle="outline-info", width=20)
        self.boton_registro.pack(pady=10)
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def iniciar_sesion(self):
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()

        # Validación de campos vacíos
        if not correo or not contrasena:
            Messagebox.show_warning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Verificación de usuario con la base de datos
        usuario = self.user_manager.verificar_usuario(correo, contrasena)

        if usuario:
            # Si el login es exitoso, muestra un mensaje y abre la aplicación de gestión de pacientes
            Messagebox.show_info("Login Exitoso", f"Bienvenido, {usuario['correo']} ({usuario['rol']})")
            self.root.withdraw()  # Oculta la ventana de login

            # Crear la ventana principal de gestión de pacientes con el usuario logueado
            registerpac_root = ttk.Toplevel(self.root)
            PatientManagementApp(registerpac_root, usuario)  # Pasar el usuario logueado
            registerpac_root.protocol("WM_DELETE_WINDOW", self.root.quit)
        else:
            # Si la autenticación falla, muestra un mensaje de error
            Messagebox.show_error("Error", "Correo o contraseña incorrectos")


    def abrir_registro(self):
        """Abre la ventana de registro y cierra la ventana de login si el registro es exitoso"""
        register_root = ttk.Toplevel(self.root)  # Crear la ventana hija de registro
        register_app = register_gui.RegisterApp(register_root, self)  # Pasa la instancia principal para control
        register_root.protocol("WM_DELETE_WINDOW", register_root.destroy)

    def mostrar_login(self):
        """Muestra la ventana de login si la ventana principal se cierra"""
        self.root.deiconify()  # Restaura la ventana de login

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = LoginApp(root)
    root.mainloop()
