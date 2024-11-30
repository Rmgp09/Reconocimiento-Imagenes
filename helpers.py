# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 18:40:26 2024

@author: Renzo Gonzales
"""

# helpers.py

def center_window(root, width, height):
    """
    Centra la ventana en la pantalla.
    
    :param root: La ventana principal o ventana de diálogo.
    :param width: Ancho de la ventana.
    :param height: Altura de la ventana.
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
