import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector
import pandas as pd
import numpy as np

# ------------------ FUNCIÓN: Conexión a la Base de Datos ------------------
def obtener_datos(query):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="renzo",
            database="sistema_dental"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return pd.DataFrame(resultados)
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return pd.DataFrame()

# ------------------ FUNCIONES PARA ACTUALIZAR SECCIONES ------------------
def limpiar_contenido():
    """
    Elimina todos los widgets dentro de main_frame y recrea los frames necesarios.
    """
    global tarjeta_frame, graficos_frame  # Aseguramos que las referencias sean globales
    for widget in main_frame.winfo_children():
        widget.destroy()
    # Recrear los frames necesarios después de limpiar
    tarjeta_frame = ttk.Frame(main_frame, padding=10)
    tarjeta_frame.pack(fill=X, padx=5, pady=5)
    graficos_frame = ttk.Frame(main_frame, padding=10)
    graficos_frame.pack(fill=BOTH, expand=True)
    

def limpiar_graficos():
    """
    Elimina los gráficos existentes dentro de graficos_frame.
    """
    for widget in graficos_frame.winfo_children():
        widget.destroy()

def mostrar_tarjetas():
    """
    Muestra las tarjetas de información en la parte superior.
    """
    pacientes = obtener_datos("SELECT COUNT(*) AS total_pacientes FROM pacientesd;")
    roles = obtener_datos("SELECT rol, COUNT(*) AS total FROM usuarios GROUP BY rol;")
    diagnosticos = obtener_datos("SELECT diagnostico, COUNT(*) AS total FROM reportesd GROUP BY diagnostico;")

    tarjetas = [
        ("Pacientes", pacientes['total_pacientes'][0] if not pacientes.empty else 0, "#2196F3", "d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen45.png"),
        ("Odontólogos", roles.loc[roles['rol'] == 'Odontólogo', 'total'].sum() if not roles.empty else 0, "#4CAF50", "d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen43.png"),
        ("Administradores", roles.loc[roles['rol'] == 'Administrador', 'total'].sum() if not roles.empty else 0, "#FFC107", "d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen46.png"),
        ("Diagnósticos", diagnosticos['total'].sum() if not diagnosticos.empty else 0, "#FF5722", "d:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/Imgenes para el diseño/imagen42.png")
    ]

    for titulo, valor, color, imagen_ruta in tarjetas:
        tarjeta = ttk.Frame(tarjeta_frame, padding=10, style="Card.TFrame")
        tarjeta.pack(side=LEFT, padx=5, pady=5, expand=True, fill=BOTH)

        app.style.configure(f"{titulo}.TFrame", background=color)
        tarjeta.configure(style=f"{titulo}.TFrame")

        contenido = ttk.Frame(tarjeta, style=f"{titulo}.TFrame")
        contenido.pack(fill=BOTH, expand=True)

        try:
            img = PhotoImage(file=imagen_ruta).subsample(6, 6)
            img_label = ttk.Label(contenido, image=img, background=color)
            img_label.image = img
            img_label.pack(side=LEFT, padx=10)
        except Exception as e:
            print(f"Error al cargar la imagen para '{titulo}': {e}")

        datos = ttk.Frame(contenido, style=f"{titulo}.TFrame")
        datos.pack(side=LEFT, fill=BOTH, expand=True)

        ttk.Label(datos, text=titulo.upper(), font="-size 12 -weight bold", foreground="white", background=color).pack(anchor="w", pady=5)
        ttk.Label(datos, text=str(valor), font="-size 20 -weight bold", foreground="white", background=color).pack(anchor="w", pady=5)

def mostrar_graficos():
    """
    Muestra los gráficos circular y de barras dinámicos.
    """
    limpiar_graficos()
    
    # Consultar datos para el gráfico circular
    sexo_distribucion = obtener_datos("SELECT sexo, COUNT(*) AS total FROM pacientesd GROUP BY sexo;")
    
    # Consultar datos para el gráfico de barras
    diagnosticos = obtener_datos("SELECT diagnostico, COUNT(*) AS total FROM reportesd GROUP BY diagnostico;")

    # --- Gráfico Circular: Distribución por Sexo ---
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    colores_sexo = ['#4CAF50', '#FF5252']  # Verde y rojo para los géneros
    valores = sexo_distribucion['total'].values if not sexo_distribucion.empty else [0, 0]
    etiquetas = sexo_distribucion['sexo'].values if not sexo_distribucion.empty else ['Sin Datos']
    explode = [0.1] + [0] * (len(valores) - 1)  # Resaltar el primer segmento
    ax1.pie(
        valores,
        labels=etiquetas,
        autopct='%1.1f%%',
        startangle=90,
        colors=colores_sexo,
        explode=explode,
        shadow=True
    )
    ax1.set_title("Distribución por Sexo", fontsize=12, weight='bold')

    canvas1 = FigureCanvasTkAgg(fig1, master=graficos_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # --- Gráfico de Barras Dinámico: Diagnósticos ---
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    
    # Preparar datos de Diagnósticos
    if not diagnosticos.empty:
        categorias = diagnosticos['diagnostico']
        valores = diagnosticos['total']
    else:
        categorias = ['Sin Datos']
        valores = [0]

    # Colores para el gráfico
    colores_barras = ['#1E88E5', '#F4511E', '#43A047', '#FB8C00', '#6A1B9A']
    colores_seleccionados = colores_barras[:len(categorias)]  # Ajustar colores a los datos disponibles

    # Crear barras
    bars = ax2.bar(categorias, valores, color=colores_seleccionados, edgecolor="black", linewidth=1.2)

    # Añadir etiquetas de valores en las barras
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2.0, height + 0.2,  # Separación vertical para legibilidad
                 f'{height}', ha='center', va='bottom', fontsize=11, color='black', weight='bold')

    # Personalización del gráfico
    ax2.set_title("Distribución de Diagnósticos", fontsize=16, weight='bold', color="#2C3E50", pad=20)  # Espaciado superior
    ax2.set_ylabel("Cantidad", fontsize=12, labelpad=10, color="#34495E")
    ax2.tick_params(axis='x', rotation=30, labelsize=10)  # Rotar etiquetas del eje X
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar margen inferior para etiquetas largas
    fig2.subplots_adjust(bottom=0.3)

    canvas2 = FigureCanvasTkAgg(fig2, master=graficos_frame)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Configuración del layout
    graficos_frame.columnconfigure(0, weight=1)
    graficos_frame.columnconfigure(1, weight=1)


def actualizar_datos():
    """
    Actualiza los datos de las tarjetas y gráficos.
    """
    limpiar_contenido()
    mostrar_tarjetas()
    mostrar_graficos()

# ------------------ CREAR VENTANA PRINCIPAL ------------------
app = ttk.Window(themename="superhero")
app.style.configure("Estadisticas.TFrame", background="white")  # Fondo blanco para la sección derecha
app.title("Sistema Dental")
app.geometry("1400x900")
app.resizable(True, True)

header = ttk.Frame(app, padding=10)
header.pack(fill=X)
ttk.Label(header, text=f"Bienvenido al Sistema Dental | Fecha: {datetime.now().strftime('%d-%m-%Y')}", font="-size 16 -weight bold").pack()

main_frame = ttk.Frame(app, padding=10)
main_frame.pack(fill=BOTH, expand=True)

tarjeta_frame = ttk.Frame(main_frame, padding=10)
tarjeta_frame.pack(fill=X, padx=5, pady=5)

graficos_frame = ttk.Frame(main_frame, padding=10)
graficos_frame.pack(fill=BOTH, expand=True)

actualizar_datos()

footer = ttk.Frame(app, padding=10)
footer.pack(fill=X)
ttk.Label(footer, text="Sistema Dental - 2024 ©", anchor=CENTER, font="-size 10 -slant italic").pack()

app.mainloop()