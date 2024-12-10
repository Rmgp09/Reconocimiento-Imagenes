import pandas as pd
import matplotlib.pyplot as plt
import logging
import numpy as np

# Configurar el logger
logging.basicConfig(
    filename="analisis_diagnostico.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Datos proporcionados
datos = {
    "Participante": [
        "Participante 1", "Participante 2", "Participante 3", "Participante 4",
        "Participante 5", "Participante 6", "Participante 7", "Participante 8",
        "Participante 9", "Participante 10"
    ],
    "Pretest: Tiempo Diagnóstico (min)": [21.23, 20.84, 21.49, 20.83, 19.31, 20.01, 18.49, 18.84, 20.90, 20.08],
    "Postest: Tiempo Diagnóstico (min)": [14.84, 14.21, 12.76, 12.21, 14.93, 12.56, 14.70, 14.89, 13.99, 12.53],
    "Pretest: Precisión (%)": [79.07, 77.19, 77.99, 73.83, 73.06, 71.44, 73.05, 79.28, 76.44, 72.15],
    "Postest: Precisión (%)": [91.84, 94.42, 94.54, 90.11, 91.48, 90.07, 90.83, 90.07, 94.87, 94.41],
    "Observaciones": [
        "Sin incidentes", "Interrupciones menores en la evaluación", "Interrupciones menores en la evaluación",
        "Sin incidentes", "Sin incidentes", "Interrupciones menores en la evaluación", "Sin incidentes",
        "Sin incidentes", "Sin incidentes", "Sin incidentes"
    ]
}

# Crear un DataFrame
df = pd.DataFrame(datos)

# Calcular el promedio y añadirlo como una fila extra
promedios = {
    "Participante": "Promedio",
    "Pretest: Tiempo Diagnóstico (min)": df["Pretest: Tiempo Diagnóstico (min)"].mean(),
    "Postest: Tiempo Diagnóstico (min)": df["Postest: Tiempo Diagnóstico (min)"].mean(),
    "Pretest: Precisión (%)": df["Pretest: Precisión (%)"].mean(),
    "Postest: Precisión (%)": df["Postest: Precisión (%)"].mean(),
    "Observaciones": ""
}
df = pd.concat([df, pd.DataFrame([promedios])], ignore_index=True)

# Guardar los datos en un archivo CSV
df.to_csv("analisis_diagnostico.csv", index=False)

# Registrar resultados en el log
logging.info("Registro de análisis de diagnóstico:")
for i, row in df.iterrows():
    if row["Participante"] == "Promedio":
        logging.info(
            f"{row['Participante']}: Promedio Tiempo Pretest: {row['Pretest: Tiempo Diagnóstico (min)']:.2f} min, "
            f"Promedio Tiempo Postest: {row['Postest: Tiempo Diagnóstico (min)']:.2f} min, "
            f"Promedio Precisión Pretest: {row['Pretest: Precisión (%)']:.2f}%, "
            f"Promedio Precisión Postest: {row['Postest: Precisión (%)']:.2f}%"
        )
    else:
        logging.info(
            f"{row['Participante']}: Tiempo Pretest: {row['Pretest: Tiempo Diagnóstico (min)']:.2f} min, "
            f"Tiempo Postest: {row['Postest: Tiempo Diagnóstico (min)']:.2f} min, "
            f"Precisión Pretest: {row['Pretest: Precisión (%)']:.2f}%, "
            f"Precisión Postest: {row['Postest: Precisión (%)']:.2f}%, "
            f"Observaciones: {row['Observaciones']}"
        )

# Mostrar los datos
print(df)

# Visualización: Comparación de precisión (Evitar superposición de barras)
x = np.arange(len(df["Participante"][:-1]))  # Índices para las barras
width = 0.35  # Ancho de las barras

plt.figure(figsize=(10, 6))
plt.bar(x - width / 2, df["Pretest: Precisión (%)"][:-1], width, label="Pretest", color="lightgreen")
plt.bar(x + width / 2, df["Postest: Precisión (%)"][:-1], width, label="Postest", color="purple")

# Añadir etiquetas de los valores
for i, v in enumerate(df["Pretest: Precisión (%)"][:-1]):
    plt.text(x[i] - width / 2, v + 0.5, f"{v:.1f}%", ha="center", va="bottom", fontsize=9)
for i, v in enumerate(df["Postest: Precisión (%)"][:-1]):
    plt.text(x[i] + width / 2, v + 0.5, f"{v:.1f}%", ha="center", va="bottom", fontsize=9)

plt.axhline(promedios["Pretest: Precisión (%)"], color='green', linestyle='--', label="Promedio Pretest")
plt.axhline(promedios["Postest: Precisión (%)"], color='brown', linestyle='--', label="Promedio Postest")
plt.title("Comparación de Precisión de Diagnóstico")
plt.xlabel("Participantes")
plt.ylabel("Precisión (%)")
plt.xticks(x, df["Participante"][:-1], rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("comparacion_precision.png")
plt.show()
