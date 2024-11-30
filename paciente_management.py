# registerpac_gui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector

# Configuración de conexión a la base de datos
db_config = {
    'user': 'root',
    'password': 'renzo',
    'host': 'localhost',
    'database': 'sistema_dental'
}

class PatientManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pacientes")
        self.root.geometry("950x400")
        
        self.setup_ui()
        self.load_patients()

    def setup_ui(self):
        # Tabla de pacientes
        columns = ("id", "DNI", "Nombres", "Apellidos", "Fecha Nacimiento", "Sexo", "Número", "Correo", "Dirección")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor="center")
        
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción centrados en la parte inferior
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Registrar Paciente", command=self.open_register_form, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Editar Paciente", command=self.open_edit_form, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Paciente", command=self.delete_patient, style="TButton").pack(side="left", padx=5)

    def load_patients(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pacientesd")
            patients_data = cursor.fetchall()

            for patient in patients_data:
                patient = list(patient)
                patient[4] = patient[4].strftime("%d-%m-%Y")  # Formato de fecha como "dd-mm-aaaa"
                self.table.insert("", "end", values=patient)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de pacientes: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_register_form(self):
        register_root = ttk.Toplevel(self.root)
        RegisterPatientForm(register_root, self)

    def open_edit_form(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un paciente para editar.")
            return

        patient_data = self.table.item(selected_item)["values"]
        edit_root = ttk.Toplevel(self.root)
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
                connection = mysql.connector.connect(**db_config)
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


class RegisterPatientForm:
    def __init__(self, root, parent_app):
        self.root = root
        self.parent_app = parent_app
        self.root.title("Registrar Paciente")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        # Campos de entrada, centrados en el formulario
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="DNI").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.dni_entry = ttk.Entry(form_frame)
        self.dni_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Nombres").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.nombres_entry = ttk.Entry(form_frame)
        self.nombres_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Apellidos").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.apellidos_entry = ttk.Entry(form_frame)
        self.apellidos_entry.grid(row=2, column=1, pady=5)

        # Fecha de Nacimiento en formato dd-mm-aaaa
        ttk.Label(form_frame, text="Fecha de Nacimiento").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        fecha_frame = ttk.Frame(form_frame)
        fecha_frame.grid(row=3, column=1, pady=5)
        self.dia_combo = ttk.Combobox(fecha_frame, values=list(range(1, 32)), width=5, state="readonly")
        self.dia_combo.set("Día")
        self.dia_combo.pack(side="left")
        self.mes_combo = ttk.Combobox(fecha_frame, values=list(range(1, 13)), width=5, state="readonly")
        self.mes_combo.set("Mes")
        self.mes_combo.pack(side="left", padx=(5, 0))
        self.ano_combo = ttk.Combobox(fecha_frame, values=list(range(1900, 2025)), width=6, state="readonly")
        self.ano_combo.set("Año")
        self.ano_combo.pack(side="left", padx=(5, 0))

        ttk.Label(form_frame, text="Sexo").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.sexo_combo = ttk.Combobox(form_frame, values=["Masculino", "Femenino"], state="readonly")
        self.sexo_combo.grid(row=4, column=1, pady=5)

        ttk.Label(form_frame, text="Número de Teléfono").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.telefono_entry = ttk.Entry(form_frame)
        self.telefono_entry.grid(row=5, column=1, pady=5)

        ttk.Label(form_frame, text="Correo").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.correo_entry = ttk.Entry(form_frame)
        self.correo_entry.grid(row=6, column=1, pady=5)

        ttk.Label(form_frame, text="Dirección").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.direccion_entry = ttk.Entry(form_frame)
        self.direccion_entry.grid(row=7, column=1, pady=5)

        ttk.Button(self.root, text="Guardar", command=self.save_patient).pack(pady=20)

    def save_patient(self):
        try:
            fecha_nacimiento = f"{int(self.ano_combo.get())}-{int(self.mes_combo.get()):02d}-{int(self.dia_combo.get()):02d}"
        except ValueError:
            messagebox.showerror("Error", "Seleccione una fecha válida.")
            return

        data = (
            self.dni_entry.get(),
            self.nombres_entry.get(),
            self.apellidos_entry.get(),
            fecha_nacimiento,
            self.sexo_combo.get(),
            self.telefono_entry.get(),
            self.correo_entry.get(),
            self.direccion_entry.get(),
        )

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = """
            INSERT INTO pacientesd (dni, nombres, apellidos, fechanacimiento, sexo, numero, correo, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, data)
            connection.commit()
            messagebox.showinfo("Éxito", "Paciente registrado.")
            self.root.destroy()
            self.parent_app.load_patients()  # Actualizar lista en ventana principal
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar el paciente: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")  # Cambiar a ttkbootstrap
    app = PatientManagementApp(root)
    root.mainloop()
