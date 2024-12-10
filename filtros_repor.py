import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd

# Función para generar el reporte
def generar_reporte():
    fecha_inicio = date_inicio.entry.get_date()
    fecha_fin = date_fin.entry.get_date()
    tipo_diag = combo_tipo_diag.get()

    if fecha_inicio > fecha_fin:
        ttk.Messagebox.show_error("Error", "La fecha de inicio no puede ser mayor que la fecha final.")
        return

    # Datos ficticios
    datos = [
        {"Fecha": "2024-12-01", "Diagnóstico": "Posible tumor", "Paciente": "Juan Pérez"},
        {"Fecha": "2024-12-02", "Diagnóstico": "Posible quiste", "Paciente": "Ana Gómez"},
        {"Fecha": "2024-12-03", "Diagnóstico": "Posible tumor", "Paciente": "Luis Martínez"},
        {"Fecha": "2024-12-04", "Diagnóstico": "Posible quiste", "Paciente": "Sofía López"},
        {"Fecha": "2024-12-05", "Diagnóstico": "Posible tumor", "Paciente": "Carlos Fernández"},
    ]

    # Crear DataFrame
    df = pd.DataFrame(datos)

    # Filtrar por rango de fechas
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df_filtrado = df[(df['Fecha'] >= pd.to_datetime(fecha_inicio)) & (df['Fecha'] <= pd.to_datetime(fecha_fin))]

    # Filtrar por tipo de diagnóstico si se seleccionó uno
    if tipo_diag != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Diagnóstico'] == tipo_diag]

    if df_filtrado.empty:
        ttk.Messagebox.show_info("Reporte", "No se encontraron datos con los filtros aplicados.")
    else:
        # Mostrar el DataFrame en una nueva ventana
        ventana_reporte = ttk.Toplevel()
        ventana_reporte.title("Reporte Generado")
        ventana_reporte.geometry("700x400")

        # Convertir el DataFrame a texto
        reporte_texto = df_filtrado.to_string(index=False)

        # Mostrar en un widget de texto
        text_reporte = ttk.Text(ventana_reporte, wrap=WORD, width=80, height=20)
        text_reporte.insert("1.0", reporte_texto)
        text_reporte.pack(padx=10, pady=10)

# Crear la ventana principal con ttkbootstrap
ventana = ttk.Window(themename="journal")
ventana.title("Interfaz de Filtros para Reportes")
ventana.geometry("500x400")

# Etiqueta para el rango de fechas
label_fecha = ttk.Label(ventana, text="Rango de Fechas:", font=("Helvetica", 12))
label_fecha.pack(pady=10)

# Selección de fecha de inicio
label_inicio = ttk.Label(ventana, text="Fecha de Inicio:", font=("Helvetica", 10))
label_inicio.pack()
date_inicio = ttk.DateEntry(ventana, bootstyle=PRIMARY, width=12)
date_inicio.pack(pady=5)

# Selección de fecha final
label_fin = ttk.Label(ventana, text="Fecha Final:", font=("Helvetica", 10))
label_fin.pack()
date_fin = ttk.DateEntry(ventana, bootstyle=PRIMARY, width=12)
date_fin.pack(pady=5)

# Selección de tipo de diagnóstico
label_tipo_diag = ttk.Label(ventana, text="Tipo de Diagnóstico:", font=("Helvetica", 12))
label_tipo_diag.pack(pady=10)
combo_tipo_diag = ttk.Combobox(ventana, values=["Todos", "Posible tumor", "Posible quiste"])
combo_tipo_diag.set("Todos")  # Valor predeterminado
combo_tipo_diag.pack()

# Botón para generar el reporte
btn_generar = ttk.Button(ventana, text="Generar Reporte", bootstyle=SUCCESS, command=generar_reporte)
btn_generar.pack(pady=20)

# Ejecutar la aplicación
ventana.mainloop()
