# registerpac_gui.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import mysql.connector
import datetime
from app_gui import DentalDetectionSystem
from datetime import datetime



class PatientManagementApp:
    def __init__(self, root, user=None):
        self.root = root
        self.user = user  # Guarda el usuario logueado para usarlo en la clase
        self.root.title("Gestión de Pacientes")
        self.root.geometry("950x600")
        
        self.center_window(self.root, 1500, 600)  # Centrar la ventana en la pantalla
        self.setup_ui()
        self.load_patients()

    def center_window(self, window, width, height):
        """Centrar la ventana especificada en la pantalla."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Campo de búsqueda
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Buscar Paciente:").pack(side="left", padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.filter_patients, style="info.TButton").pack(side="left", padx=(5, 0))
        ttk.Button(search_frame, text="Mostrar Todo", command=self.load_patients, style="secondary.TButton").pack(side="left", padx=(5, 0))

                # Configuración de estilo para la tabla (Treeview)
        style = ttk.Style()

        # Estilo general para la tabla
        style.configure(
            "Treeview",
            font=("Helvetica", 10),                # Fuente del contenido
            rowheight=30,                          # Altura de las filas
            background="#222831",                  # Fondo gris oscuro para las filas
            foreground="#e0e0e0",                  # Texto claro
            fieldbackground="#222831",             # Fondo de las celdas
            borderwidth=0                          # Sin bordes externos
        )

        # Líneas divisorias entre las filas
        style.configure(
            "Treeview",
            relief="flat",                         # Sin relieve para el área general
            highlightthickness=1,                  # Grosor de las líneas divisorias
            highlightbackground="#393e46"         # Color de las líneas entre filas
        )

        # Estilo para las filas seleccionadas
        style.map(
            "Treeview",
            background=[("selected", "#00adb5")],  # Fondo turquesa vibrante para la fila seleccionada
            foreground=[("selected", "#ffffff")]   # Texto blanco para la fila seleccionada
        )

        # Estilo para los encabezados de la tabla
        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 11, "bold"),        # Fuente de los encabezados
            background="#393e46",                  # Fondo gris medio
            foreground="#ffffff",                  # Texto blanco
            borderwidth=1,                         # Borde fino para el encabezado
            relief="raised"                        # Relieve elevado para destacar
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#1b2025")],    # Fondo gris más oscuro al pasar el ratón
            relief=[("pressed", "sunken")]         # Relieve hundido al presionar
        )

        # Creación de la tabla con las columnas
        columns = ("id", "DNI", "Nombres", "Apellidos", "Fecha Nacimiento", "Sexo", "Número", "Correo", "Dirección")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")

        # Configuración de encabezados y columnas
        for col in columns:
            self.table.heading(col, text=col, anchor="center")  # Encabezados centrados
            self.table.column(col, width=120, anchor="center")  # Columnas centradas

        # Agregar margen y espacio alrededor de la tabla
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        button_frame.place(relx=0.5, rely=0.92, anchor="center")

        # Cargar y redimensionar íconos para los botones
        self.add_icon = ImageTk.PhotoImage(Image.open("d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen54.png").resize((30, 30)))
        self.edit_icon = ImageTk.PhotoImage(Image.open("d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen50.png").resize((30, 30)))
        self.delete_icon = ImageTk.PhotoImage(Image.open("d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen48.png").resize((30, 30)))
        self.diagnose_icon = ImageTk.PhotoImage(Image.open("d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen35.png").resize((30, 30)))

        ttk.Button(button_frame, text="Registrar Paciente", image=self.add_icon, compound="left", command=self.open_register_form, style="success.TButton", width=18).pack(side="left", padx=10, pady=10)
        ttk.Button(button_frame, text="Editar Paciente", image=self.edit_icon, compound="left", command=self.open_edit_form, style="primary.TButton", width=18).pack(side="left", padx=10, pady=10)
        ttk.Button(button_frame, text="Eliminar Paciente", image=self.delete_icon, compound="left", command=self.delete_patient, style="danger.TButton", width=18).pack(side="left", padx=10, pady=10)
        ttk.Button(button_frame, text="Diagnosticar", image=self.diagnose_icon, compound="left", command=self.open_diagnose_form, style="info.TButton", width=18).pack(side="left", padx=10, pady=10)

        style = ttk.Style()

        # Configuración de cada estilo visual mejorado
        style.configure("success.TButton", background="#28a745", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=2, relief="ridge")
        style.map("success.TButton", background=[("active", "#218838")], relief=[("pressed", "sunken")])

        style.configure("primary.TButton", background="#007bff", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=2, relief="ridge")
        style.map("primary.TButton", background=[("active", "#0056b3")], relief=[("pressed", "sunken")])

        style.configure("danger.TButton", background="#dc3545", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=2, relief="ridge")
        style.map("danger.TButton", background=[("active", "#c82333")], relief=[("pressed", "sunken")])

        style.configure("info.TButton", background="#17a2b8", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=2, relief="ridge")
        style.map("info.TButton", background=[("active", "#138496")], relief=[("pressed", "sunken")])


    def load_patients(self):
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="renzo",
                database="sistema_dental"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pacientesd")
            patients_data = cursor.fetchall()

            for patient in patients_data:
                patient = list(patient)
                patient[4] = patient[4].strftime("%d-%m-%Y")
                self.table.insert("", "end", values=patient)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de pacientes: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def filter_patients(self):
        """Filtrar pacientes basado en el término de búsqueda."""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.")
            return

        # Limpiar la tabla antes de mostrar los resultados de búsqueda
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="renzo",
                database="sistema_dental"
            )
            cursor = connection.cursor()
            query = """
            SELECT * FROM pacientesd 
            WHERE DNI LIKE %s OR Nombres LIKE %s OR Apellidos LIKE %s
            """
            search_query = f"%{search_term}%"
            cursor.execute(query, (search_query, search_query, search_query))
            patients_data = cursor.fetchall()

            for patient in patients_data:
                patient = list(patient)
                patient[4] = patient[4].strftime("%d-%m-%Y")
                self.table.insert("", "end", values=patient)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_register_form(self):
        register_root = ttk.Toplevel(self.root)
        self.center_window(register_root, 400, 750)
        RegisterPatientForm(register_root, self)

    def open_edit_form(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un paciente para editar.")
            return

        patient_data = self.table.item(selected_item)["values"]
        edit_root = ttk.Toplevel(self.root)
        self.center_window(edit_root, 400, 600)
        EditPatientForm(edit_root, self, patient_data)

    def delete_patient(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un paciente para eliminar.")
            return

        patient_id = self.table.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este paciente?")
        if confirm:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="renzo",
                    database="sistema_dental"
                )
                cursor = connection.cursor()
                cursor.execute("DELETE FROM pacientesd WHERE id = %s", (patient_id,))
                connection.commit()
                self.load_patients()
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo eliminar el paciente: {err}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()



    def open_diagnose_form(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un paciente para diagnosticar.")
            return

        patient_data = self.table.item(selected_item)["values"]

        # Calcular la edad del paciente a partir de la fecha de nacimiento
        fecha_nacimiento_str = patient_data[4]  # Fecha de nacimiento en formato "dd-mm-aaaa"
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%d-%m-%Y")
        edad = datetime.now().year - fecha_nacimiento.year
        if (datetime.now().month, datetime.now().day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1  # Ajustar la edad si aún no ha cumplido el año en curso

        # Crear la ventana para el diagnóstico y pasar la información del paciente seleccionado
        diagnose_root = Toplevel(self.root)
        DentalDetectionSystem(diagnose_root, user=self.user, patient={
            "nombre_completo": f"{patient_data[2]} {patient_data[3]}",  # Nombres y apellidos
            "dni": patient_data[1],  # DNI
            "edad": edad,            # Edad calculada
        })
        self.center_window(diagnose_root, 1000, 700)  # Centrar la ventana del diagnóstico

class RegisterPatientForm:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Registrar Paciente")
        self.root.geometry("400x750")
        self.app.center_window(self.root, 400, 700)

        ttk.Label(root, text="DNI").pack(pady=5)
        self.dni_entry = ttk.Entry(root)
        self.dni_entry.pack(pady=5)

        ttk.Label(root, text="Nombres").pack(pady=5)
        self.nombres_entry = ttk.Entry(root)
        self.nombres_entry.pack(pady=5)

        ttk.Label(root, text="Apellidos").pack(pady=5)
        self.apellidos_entry = ttk.Entry(root)
        self.apellidos_entry.pack(pady=5)

        ttk.Label(root, text="Fecha de Nacimiento").pack(pady=5)
        date_frame = ttk.Frame(root)
        date_frame.pack(pady=5)

        self.day_combobox = ttk.Combobox(date_frame, width=5, values=[str(i).zfill(2) for i in range(1, 32)], state="readonly")
        self.day_combobox.set("Día")
        self.day_combobox.pack(side="left", padx=2)

        self.month_combobox = ttk.Combobox(date_frame, width=5, values=[str(i).zfill(2) for i in range(1, 13)], state="readonly")
        self.month_combobox.set("Mes")
        self.month_combobox.pack(side="left", padx=2)

        self.year_combobox = ttk.Combobox(date_frame, width=7, values=[str(i) for i in range(1900, datetime.now().year + 1)], state="readonly")
        self.year_combobox.set("Año")
        self.year_combobox.pack(side="left", padx=2)

        ttk.Label(root, text="Género").pack(pady=5)
        self.sexo_combobox = ttk.Combobox(root, values=["Masculino", "Femenino"], state="readonly")
        self.sexo_combobox.pack(pady=5)

        ttk.Label(root, text="Número de Teléfono").pack(pady=5)
        self.numero_entry = ttk.Entry(root)
        self.numero_entry.pack(pady=5)

        ttk.Label(root, text="Correo Electrónico").pack(pady=5)
        self.correo_entry = ttk.Entry(root)
        self.correo_entry.pack(pady=5)

        ttk.Label(root, text="Dirección").pack(pady=5)
        self.direccion_entry = ttk.Entry(root)
        self.direccion_entry.pack(pady=5)

        ttk.Button(root, text="Guardar", command=self.register_patient, style="success.TButton").pack(pady=10)

    def register_patient(self):
        dni = self.dni_entry.get()
        nombres = self.nombres_entry.get()
        apellidos = self.apellidos_entry.get()
        day = self.day_combobox.get()
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        sexo = self.sexo_combobox.get()
        numero = self.numero_entry.get()
        correo = self.correo_entry.get()
        direccion = self.direccion_entry.get()

        if day.isdigit() and month.isdigit() and year.isdigit():
            fecha_nacimiento = f"{year}-{month}-{day}"
        else:
            messagebox.showerror("Error", "Fecha de nacimiento inválida.")
            return

        if not all([dni, nombres, apellidos, sexo, numero, correo, direccion]):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="renzo",
                database="sistema_dental"
            )
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO pacientesd (DNI, Nombres, Apellidos, FechaNacimiento, Sexo, Numero, Correo, Direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (dni, nombres, apellidos, fecha_nacimiento, sexo, numero, correo, direccion))
            connection.commit()
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            self.root.destroy()
            self.app.load_patients()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar el paciente: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class EditPatientForm:
    def __init__(self, root, app, patient_data):
        self.root = root
        self.app = app
        self.patient_id = patient_data[0]
        self.root.title("Editar Paciente")
        self.root.geometry("400x750")
        self.app.center_window(self.root, 400, 700)

        ttk.Label(root, text="DNI").pack(pady=5)
        self.dni_entry = ttk.Entry(root)
        self.dni_entry.insert(0, patient_data[1])
        self.dni_entry.pack(pady=5)

        ttk.Label(root, text="Nombres").pack(pady=5)
        self.nombres_entry = ttk.Entry(root)
        self.nombres_entry.insert(0, patient_data[2])
        self.nombres_entry.pack(pady=5)

        ttk.Label(root, text="Apellidos").pack(pady=5)
        self.apellidos_entry = ttk.Entry(root)
        self.apellidos_entry.insert(0, patient_data[3])
        self.apellidos_entry.pack(pady=5)

        ttk.Label(root, text="Fecha de Nacimiento").pack(pady=5)
        date_frame = ttk.Frame(root)
        date_frame.pack(pady=5)

        day, month, year = patient_data[4].split("-")
        self.day_combobox = ttk.Combobox(date_frame, width=5, values=[str(i).zfill(2) for i in range(1, 32)], state="readonly")
        self.day_combobox.set(day)
        self.day_combobox.pack(side="left", padx=2)

        self.month_combobox = ttk.Combobox(date_frame, width=5, values=[str(i).zfill(2) for i in range(1, 13)], state="readonly")
        self.month_combobox.set(month)
        self.month_combobox.pack(side="left", padx=2)

        self.year_combobox = ttk.Combobox(date_frame, width=7, values=[str(i) for i in range(1900, datetime.now().year + 1)], state="readonly")
        self.year_combobox.set(year)
        self.year_combobox.pack(side="left", padx=2)

        ttk.Label(root, text="Sexo").pack(pady=5)
        self.sexo_combobox = ttk.Combobox(root, values=["Masculino", "Femenino"], state="readonly")
        self.sexo_combobox.set(patient_data[5])
        self.sexo_combobox.pack(pady=5)

        ttk.Label(root, text="Número de Teléfono").pack(pady=5)
        self.numero_entry = ttk.Entry(root)
        self.numero_entry.insert(0, patient_data[6])
        self.numero_entry.pack(pady=5)

        ttk.Label(root, text="Correo Electrónico").pack(pady=5)
        self.correo_entry = ttk.Entry(root)
        self.correo_entry.insert(0, patient_data[7])
        self.correo_entry.pack(pady=5)

        ttk.Label(root, text="Dirección").pack(pady=5)
        self.direccion_entry = ttk.Entry(root)
        self.direccion_entry.insert(0, patient_data[8])
        self.direccion_entry.pack(pady=5)

        ttk.Button(root, text="Guardar Cambios", command=self.update_patient, style="success.TButton").pack(pady=10)

    def update_patient(self):
        dni = self.dni_entry.get()
        nombres = self.nombres_entry.get()
        apellidos = self.apellidos_entry.get()
        day = self.day_combobox.get()
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        sexo = self.sexo_combobox.get()
        numero = self.numero_entry.get()
        correo = self.correo_entry.get()
        direccion = self.direccion_entry.get()

        if day.isdigit() and month.isdigit() and year.isdigit():
            fecha_nacimiento = f"{year}-{month}-{day}"
        else:
            messagebox.showerror("Error", "Fecha de nacimiento inválida.")
            return

        if not all([dni, nombres, apellidos, sexo, numero, correo, direccion]):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="renzo",
                database="sistema_dental"
            )
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE pacientesd
                SET DNI=%s, Nombres=%s, Apellidos=%s, FechaNacimiento=%s, Sexo=%s, Numero=%s, Correo=%s, Direccion=%s
                WHERE id=%s
            """, (dni, nombres, apellidos, fecha_nacimiento, sexo, numero, correo, direccion, self.patient_id))
            connection.commit()
            messagebox.showinfo("Éxito", "Paciente editado correctamente.")
            self.root.destroy()
            self.app.load_patients()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo actualizar el paciente: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = PatientManagementApp(root)
    root.mainloop()
