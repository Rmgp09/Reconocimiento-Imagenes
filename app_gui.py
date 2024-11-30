# app_gui.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Menu, Toplevel
from PIL import Image, ImageTk
import cv2
import datetime
import image_processing as ip
import patient_management as pm
import user_management as um  # Asegúrate de que user_management esté importado
from reportlab.pdfgen import canvas 
import mysql.connector
from io import BytesIO
import uuid

class DentalDetectionSystem:
    def __init__(self, root, user=None, patient=None):
        self.root = root
        self.root.title("Sistema de Detección Dental")
        self.root.geometry("900x600")
        self.style = ttk.Style("superhero")
        self.center_window(self.root, 1000, 700)

        # Crear instancia de UserManager para manejar el usuario
        self.user_manager = um.UserManager()

        # Inicializar variables y módulos
        self.logged_in_user = user  # Usuario logueado
        self.current_patient = patient  # Paciente seleccionado para diagnóstico (puede ser None)
        self.image_processor = ip.ImageProcessor()
        self.patient_manager = pm.PatientManager()

        # Crear menú y configuración visual
        self.create_menu()
        self.setup_ui()

        # Variables para la imagen
        self.original_image = None
        self.processed_image = None

    def center_window(self, window, width, height):
        """Centrar la ventana en la pantalla."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Crear un contenedor para centrar los botones y la información del usuario
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # Botones de interacción con íconos y ajuste de tamaño
        self.icon_load = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen32.png").resize((25, 25)))
        self.icon_process = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen35.png").resize((25, 25)))
        self.user_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen15.png").resize((50, 50)))


        # Mostrar información del paciente seleccionado (si existe)
        if self.current_patient:
            patient_info = f"Paciente: {self.current_patient.get('nombre_completo', 'N/A')}   DNI: {self.current_patient.get('dni', 'N/A')}   Edad: {self.current_patient.get('edad', 'N/A')}"
        else:
            patient_info = "Paciente: No seleccionado"

        ttk.Label(main_frame, text=patient_info, font=("Arial", 12), bootstyle="inverse-primary").grid(row=0, column=0, columnspan=3, pady=5)

        # Botón de cargar imagen
        self.btn_load = ttk.Button(
            main_frame, text="Cargar Imagen", image=self.icon_load, compound="left", 
            command=self.load_image, bootstyle=PRIMARY, width=20
        )
        self.btn_load.grid(row=1, column=0, padx=10, pady=10)

        # Botón de procesar imagen
        self.btn_process = ttk.Button(
            main_frame, text="Procesar Imagen", image=self.icon_process, compound="left", 
            command=self.detect_anomalies, bootstyle=SUCCESS, width=20
        )
        self.btn_process.grid(row=1, column=1, padx=10, pady=10)

        # Contenedor para la imagen y el correo del usuario logueado
        user_frame = ttk.Frame(main_frame)
        user_frame.grid(row=1, column=2, padx=10, pady=10)

        # Imagen de perfil
        ttk.Label(user_frame, image=self.user_icon).pack(side="top", anchor="center")
        email = self.logged_in_user.get("correo", "Correo no disponible")
        ttk.Label(user_frame, text=email, bootstyle="inverse-primary", font=("Arial", 10)).pack(side="top", anchor="center")

        # Ajuste de columnas para centrar elementos en el frame principal
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
       

        # Panel de imágenes
        self.frame_images = ttk.Frame(self.root)
        self.frame_images.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Panel para mostrar la imagen original
        self.original_frame = ttk.LabelFrame(self.frame_images, text="Imagen Original", bootstyle="info")
        self.original_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.panel_original = ttk.Label(self.original_frame)
        self.panel_original.pack()

        # Panel para mostrar la imagen procesada
        self.processed_frame = ttk.LabelFrame(self.frame_images, text="Imagen Procesada", bootstyle="info")
        self.processed_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.panel_processed = ttk.Label(self.processed_frame)
        self.panel_processed.pack()

        # Botón para generar el reporte, debajo de las imágenes
        self.btn_generate_report = ttk.Button(
            self.root,
            text="Generar Reporte",
            bootstyle="info",
            command=self.generate_clinical_report  # Llama al método de generación
        )
        self.btn_generate_report.grid(row=3, column=0, columnspan=3, pady=20, sticky="n")

    def create_menu(self):
        menu_bar = Menu(self.root)

        # Menú Archivo
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Cargar Imagen", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Perfil del Usuario
        profile_menu = Menu(menu_bar, tearoff=0)
        profile_menu.add_command(label="Ver Perfil", command=self.view_profile)
        profile_menu.add_command(label="Editar Perfil", command=self.edit_profile)
        menu_bar.add_cascade(label="Perfil", menu=profile_menu)

        self.root.config(menu=menu_bar)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = self.image_processor.load_image(file_path)
            if self.original_image is not None:
                self.display_image(self.original_image, self.panel_original)
            else:
                messagebox.showerror("Error", "No se pudo cargar la imagen.")

    def detect_anomalies(self):
        if self.original_image is not None:
            result_image, diagnosis = self.image_processor.detect_anomalies(self.original_image)
            if result_image is not None:
                self.processed_image = result_image  # Asignar la imagen procesada
                self.display_image(result_image, self.panel_processed)
                self.patient_manager.store_diagnosis(diagnosis)
                messagebox.showinfo("Diagnóstico", diagnosis)
            else:
                messagebox.showerror("Error", "No se pudo procesar la imagen.")
        else:
            messagebox.showerror("Error", "Cargue una imagen primero.")

    def display_image(self, img, panel):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb).resize((350, 350))
        img_tk = ImageTk.PhotoImage(img_pil)
        panel.configure(image=img_tk)
        panel.image = img_tk
    def view_profile(self):
        profile_window = Toplevel(self.root)
        profile_window.title("Perfil del Usuario")
        profile_window.geometry("450x400")
        self.center_window(profile_window, 450, 400)

        # Cargar imagen de perfil
        profile_icon = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen15.png").resize((100, 100)))
        ttk.Label(profile_window, image=profile_icon).pack(pady=10)

        # Contenedor de información
        info_frame = ttk.Frame(profile_window)
        info_frame.pack(pady=10, padx=20)

        full_name = f"{self.logged_in_user.get('first_name', 'N/A')} {self.logged_in_user.get('last_name', 'N/A')}"
        email = self.logged_in_user.get("correo", "N/A")
        phone_number = self.logged_in_user.get("phone_number", "N/A")
        
        # Cambiamos el formato de la fecha a día-mes-año
        birthdate = self.logged_in_user.get("fecha_nacimiento", "N/A")
        if birthdate != "N/A":
            try:
                birthdate = f"{birthdate[8:10]}-{birthdate[5:7]}-{birthdate[:4]}"
            except Exception as e:
                print(f"Error formateando la fecha: {e}")

        role = self.logged_in_user.get("rol", "N/A")

        # Cargar iconos
        icon_name = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen37.png").resize((20, 20)))
        icon_email = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen23.png").resize((20, 20)))
        icon_phone = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen38.png").resize((20, 20)))
        icon_birthdate = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen39.png").resize((20, 20)))
        icon_role = ImageTk.PhotoImage(Image.open("d:\\Documentos\\deep learning para vison artificial\\Imgenes de dentaduras\\Imgenes para el diseño\\imagen40.png").resize((20, 20)))

        # Mostrar información
        ttk.Label(info_frame, text="Nombre Completo:", image=icon_name, compound="left", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(info_frame, text=full_name, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w", padx=10)
        ttk.Label(info_frame, text="Correo Electrónico:", image=icon_email, compound="left", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(info_frame, text=email, font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="w", padx=10)
        ttk.Label(info_frame, text="Número de Teléfono:", image=icon_phone, compound="left", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        ttk.Label(info_frame, text=phone_number, font=("Arial", 12, "bold")).grid(row=2, column=1, sticky="w", padx=10)
        ttk.Label(info_frame, text="Fecha de Nacimiento:", image=icon_birthdate, compound="left", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=5)
        ttk.Label(info_frame, text=birthdate, font=("Arial", 12, "bold")).grid(row=3, column=1, sticky="w", padx=10)
        ttk.Label(info_frame, text="Rol:", image=icon_role, compound="left", font=("Arial", 12)).grid(row=4, column=0, sticky="e", pady=5)
        ttk.Label(info_frame, text=role, font=("Arial", 12, "bold")).grid(row=4, column=1, sticky="w", padx=10)

        profile_window.icon_name = icon_name
        profile_window.icon_email = icon_email
        profile_window.icon_phone = icon_phone
        profile_window.icon_birthdate = icon_birthdate
        profile_window.icon_role = icon_role
        profile_window.profile_icon = profile_icon

    def edit_profile(self):
        edit_window = Toplevel(self.root)
        edit_window.title("Editar Perfil")
        edit_window.geometry("400x300")
        self.center_window(edit_window, 400, 300)

        info_frame = ttk.Frame(edit_window)
        info_frame.pack(pady=10, padx=20)

        # Campos de entrada
        ttk.Label(info_frame, text="Nombre:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        entry_first_name = ttk.Entry(info_frame, font=("Arial", 12))
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)
        entry_first_name.insert(0, self.logged_in_user.get("first_name", ""))

        ttk.Label(info_frame, text="Apellido:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        entry_last_name = ttk.Entry(info_frame, font=("Arial", 12))
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)
        entry_last_name.insert(0, self.logged_in_user.get("last_name", ""))

        ttk.Label(info_frame, text="Teléfono:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        entry_phone = ttk.Entry(info_frame, font=("Arial", 12))
        entry_phone.grid(row=2, column=1, padx=10, pady=5)
        entry_phone.insert(0, self.logged_in_user.get("phone_number", ""))

        save_button = ttk.Button(edit_window, text="Guardar Cambios", bootstyle="success", command=lambda: self.save_changes(entry_first_name, entry_last_name, entry_phone))
        save_button.pack(pady=10)

    def save_changes(self, entry_first_name, entry_last_name, entry_phone):
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        phone = entry_phone.get()

        if self.user_manager.update_user(self.logged_in_user["correo"], first_name, last_name, phone):
            messagebox.showinfo("Éxito", "Perfil actualizado exitosamente.")
            self.logged_in_user["first_name"] = first_name
            self.logged_in_user["last_name"] = last_name
            self.logged_in_user["phone_number"] = phone
        else:
            messagebox.showerror("Error", "No se pudo actualizar el perfil.")

    def calculate_age(self, birthdate_str):
        """Calcular la edad basado en la fecha de nacimiento en formato 'YYYY-MM-DD'"""
        try:
            birthdate = datetime.datetime.strptime(birthdate_str, "%Y-%m-%d")
            today = datetime.datetime.today()
            return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        except ValueError:
            return "Desconocido"  # Si el formato de la fecha es incorrecto

    def generate_clinical_report(self):
        """Generar un reporte clínico detallado y guardar su referencia lógica en la base de datos."""
        # Verificar que se haya seleccionado un paciente
        if self.current_patient is None:
            messagebox.showerror("Error", "No se ha seleccionado un paciente.")
            return

        # Verificar que se haya procesado una imagen
        if self.processed_image is None:
            messagebox.showerror("Error", "No se ha procesado ninguna imagen.")
            return

        # Información del paciente y odontólogo
        patient_name = self.current_patient.get("nombre_completo", "N/A")
        patient_dni = self.current_patient.get("dni", "N/A")
        patient_age = self.calculate_age(self.current_patient.get("fecha_nacimiento", "N/A"))
        dentist_name = f"{self.logged_in_user.get('first_name', '')} {self.logged_in_user.get('last_name', '')}"
        dentist_email = self.logged_in_user.get("correo", "N/A")
        diagnosis = "Posible anomalía detectada"
        observations = "La región superior presenta signos de desgaste dental."
        report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generar el PDF en memoria y guardar su referencia lógica
        self.generate_pdf_report_with_path(
            patient_name, patient_dni, patient_age,
            dentist_name, dentist_email, diagnosis,
            observations, report_date
        )


    def generate_pdf_report_with_path(self, patient_name, patient_dni, patient_age,
                                    dentist_name, dentist_email, diagnosis,
                                    observations, report_date):
        """Generar un reporte clínico en PDF y guardar su referencia lógica en la base de datos."""
        # Crear el PDF en un buffer de memoria
        buffer = BytesIO()
        c = canvas.Canvas(buffer)

        # Título del reporte
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 800, "Reporte Clínico Dental")

        # Datos del paciente
        c.setFont("Helvetica", 12)
        c.drawString(50, 750, f"Paciente: {patient_name}")
        c.drawString(50, 730, f"DNI: {patient_dni}")
        c.drawString(50, 710, f"Edad: {patient_age} años")

        # Datos del odontólogo
        c.drawString(50, 680, f"Odontólogo: {dentist_name}")
        c.drawString(50, 660, f"Correo: {dentist_email}")

        # Diagnóstico y observaciones
        c.drawString(50, 630, f"Diagnóstico: {diagnosis}")
        c.drawString(50, 610, "Observaciones:")
        c.drawString(70, 590, observations)

        # Fecha del reporte
        c.drawString(50, 560, f"Fecha del Reporte: {report_date}")

        # Finalizar el PDF en el buffer
        c.save()
        buffer.seek(0)  # Volver al inicio del buffer

        # Generar una referencia lógica para `pdf_path`
        pdf_reference = str(uuid.uuid4()) + ".pdf"  # Usar un UUID único como referencia

        # Guardar el reporte en la base de datos
        self.save_report_to_db_with_path(
            paciente_id=self.current_patient.get("id", 0),
            diagnostico=diagnosis,
            observaciones=observations,
            pdf_path=pdf_reference  # Guardar el nombre lógico en pdf_path
        )

        messagebox.showinfo("Éxito", f"Reporte generado y guardado con referencia {pdf_reference}.")

    import mysql.connector

    def save_report_to_db_with_path(self, paciente_id, diagnostico, observaciones, pdf_path):
        """Guardar el reporte en la base de datos con la referencia lógica del PDF."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="sistema_dental",
                user="root",  # Cambia por tu usuario
                password="renzo"  # Cambia por tu contraseña
            )

            if connection.is_connected():
                cursor = connection.cursor()

                # Insertar el reporte con la referencia en pdf_path
                sql_query = """
                INSERT INTO reportes (paciente_id, diagnostico, observaciones, pdf_path)
                VALUES (%s, %s, %s, %s)
                """
                data = (paciente_id, diagnostico, observaciones, pdf_path)
                cursor.execute(sql_query, data)
                connection.commit()

                print(f"Reporte guardado exitosamente con ID: {cursor.lastrowid}")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar el reporte: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    user = {
        "correo": "usuario@example.com",
        "first_name": "Renzo",
        "last_name": "Gonzales",
        "phone_number": "9874512634",
        "fecha_nacimiento": "1932-05-03",
        "rol": "Odontólogo"
    }
    app = DentalDetectionSystem(root, user)
    root.mainloop()
