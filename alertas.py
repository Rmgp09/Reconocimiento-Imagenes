from ttkbootstrap import ttk
from ttkbootstrap import Window
from ttkbootstrap.constants import *
from datetime import datetime
from tkinter import Toplevel

# Ventana principal
root = Window(themename="superhero")
root.title("Alertas Preventivas - Sistema Odontológico")
root.geometry("900x600")
root.resizable(False, False)

# Variable global para almacenar la alerta actual
alerta_actual = {}

# Función para generar una alerta automáticamente
def generar_alerta():
    global alerta_actual  # Declarar como global para poder actualizarla
    
    # Datos de ejemplo
    tipo_anomalia = "Posible Tumor en la mandíbula"
    fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    recomendacion = "Se recomienda realizar más estudios como tomografía para confirmar el diagnóstico."
    paciente = "Genesis Milagros Gonzales Pacherrez"
    edad = "15 años"

    # Actualizar la alerta actual
    alerta_actual = {
        "tipo_anomalia": tipo_anomalia,
        "fecha": fecha,
        "paciente": paciente,
        "edad": edad,
        "recomendacion": recomendacion,
    }

    # Mostrar detalles de la alerta en el marco
    alerta_label.config(text=f"⚠️ ALERTA: {tipo_anomalia}")
    detalle_label.config(
        text=f"Paciente: {paciente}\nEdad: {edad}\nFecha: {fecha}\nRecomendación: {recomendacion}"
    )

    # Agregar la alerta al historial
    historial_tree.insert("", "end", values=(tipo_anomalia, fecha, "No Resuelta"))

    # Mostrar el marco de alerta
    alerta_frame.place(relx=0.5, rely=0.5, anchor="center")

# Función para cerrar la alerta actual
def cerrar_alerta():
    alerta_frame.place_forget()

# Función para mostrar los detalles de la alerta actual
def ver_detalles():
    if not alerta_actual:
        return  # No hay alerta activa

    # Crear una ventana emergente para mostrar los detalles
    detalle_win = Toplevel(root)
    detalle_win.title("Detalles de la Alerta")
    detalle_win.geometry("400x300")
    detalle_win.resizable(False, False)

    # Información detallada
    tipo_anomalia = alerta_actual["tipo_anomalia"]
    fecha = alerta_actual["fecha"]
    paciente = alerta_actual["paciente"]
    edad = alerta_actual["edad"]
    recomendacion = alerta_actual["recomendacion"]

    # Etiquetas en la ventana emergente
    ttk.Label(detalle_win, text="Detalles de la Alerta", font=("Helvetica", 14, "bold")).pack(pady=10)
    ttk.Label(detalle_win, text=f"Tipo de Anomalía: {tipo_anomalia}", wraplength=380).pack(anchor="w", padx=10, pady=5)
    ttk.Label(detalle_win, text=f"Paciente: {paciente}", wraplength=380).pack(anchor="w", padx=10, pady=5)
    ttk.Label(detalle_win, text=f"Edad: {edad}", wraplength=380).pack(anchor="w", padx=10, pady=5)
    ttk.Label(detalle_win, text=f"Fecha: {fecha}", wraplength=380).pack(anchor="w", padx=10, pady=5)
    ttk.Label(detalle_win, text=f"Recomendación: {recomendacion}", wraplength=380).pack(anchor="w", padx=10, pady=5)

    # Botón para cerrar la ventana emergente
    ttk.Button(detalle_win, text="Cerrar", bootstyle=SECONDARY, command=detalle_win.destroy).pack(pady=10)

# Marco de alerta emergente
alerta_frame = ttk.Frame(root, padding=20, relief="ridge", style="info.TFrame")
alerta_frame.place_forget()

# Etiquetas para mostrar los detalles de la alerta
alerta_label = ttk.Label(alerta_frame, text="", font=("Helvetica", 14, "bold"), style="info.TLabel")
alerta_label.pack(anchor="w", pady=5)

detalle_label = ttk.Label(alerta_frame, text="", font=("Helvetica", 12), style="info.TLabel")
detalle_label.pack(anchor="w", pady=5)

# Botones dentro del marco de alerta
botones_frame = ttk.Frame(alerta_frame)
botones_frame.pack(pady=10, fill="x")

btn_aceptar = ttk.Button(botones_frame, text="Aceptar", bootstyle=(SUCCESS, OUTLINE), command=cerrar_alerta)
btn_aceptar.pack(side="left", expand=True, padx=5)

btn_detalle = ttk.Button(botones_frame, text="Ver Detalles", bootstyle=(INFO, OUTLINE), command=ver_detalles)
btn_detalle.pack(side="left", expand=True, padx=5)

# Tabla de historial de alertas
historial_label = ttk.Label(root, text="Historial de Alertas", font=("Helvetica", 14, "bold"), style="info.TLabel")
historial_label.pack(pady=10)

historial_tree = ttk.Treeview(
    root, columns=("Anomalía", "Fecha", "Estado"), show="headings", height=10
)
historial_tree.pack(fill="both", expand=True, padx=20, pady=10)

# Configuración de las columnas
historial_tree.heading("Anomalía", text="Anomalía")
historial_tree.heading("Fecha", text="Fecha")
historial_tree.heading("Estado", text="Estado")

historial_tree.column("Anomalía", width=300, anchor="center")
historial_tree.column("Fecha", width=200, anchor="center")
historial_tree.column("Estado", width=100, anchor="center")

# Agregar datos ficticios al historial
datos_ficticios = [
    ("Posible Tumor en la mandíbula", "04-12-2024 10:35:21", "No Resuelta"),
    ("Posible Quiste Dental", "03-12-2024 14:20:15", "Resuelta"),
    ("Posible Tumor en la mandíbula", "01-12-2024 09:15:10", "No Resuelta"),
    ("Posible Quiste Dental", "30-11-2024 12:45:50", "Resuelta"),
]

for dato in datos_ficticios:
    historial_tree.insert("", "end", values=dato)

# Botón para generar una alerta
btn_generar_alerta = ttk.Button(root, text="Generar Alerta", bootstyle=(PRIMARY, OUTLINE), command=generar_alerta)
btn_generar_alerta.pack(pady=10)

# Estilo de la interfaz
style = ttk.Style()
style.configure("info.TFrame", background="#4FC3F7", borderwidth=3)
style.configure("info.TLabel", foreground="white", background="#4FC3F7")

# Iniciar la interfaz
root.mainloop()
