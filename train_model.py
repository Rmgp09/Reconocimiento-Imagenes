# train_model.py

# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 11:38:28 2024

@author: Renzo Gonzales
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Configuraciones
image_size = (128, 128)
batch_size = 32
epochs = 10

# Configura la ruta a tus datos de entrenamiento y validación
train_dir = 'D:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/train_dir'  # Contiene subcarpetas 'quiste' y 'tumor'
validation_dir = 'D:/Documentos/deep learning para vison artificial/Imgenes de dentaduras/validation_dir'

# Generadores de datos
train_datagen = ImageDataGenerator(rescale=1.0/255.0)
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode="binary"
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode="binary"
)

# Creación del modelo CNN
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(256, activation="relu"),
    Dropout(0.5),
    Dense(1, activation="sigmoid")  # Clasificación binaria
])

# Compilación del modelo
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Entrenamiento del modelo
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator
)

# Guardar el modelo entrenado
model.save("tumor_cyst_detector.h5")
print("Modelo guardado como 'tumor_cyst_detector.h5'")
