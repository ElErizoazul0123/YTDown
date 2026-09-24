import ctypes
from ctypes import wintypes
import os

def cargar_fuente_personalizada(ruta_fuente):
    """
    Carga una fuente externa en memoria para que Tkinter pueda usarla.
    Solo funciona en Windows.
    """
    # Verifica que el archivo exista
    if not os.path.exists(ruta_fuente):
        print(f"Error: No se encontró la fuente en {ruta_fuente}")
        return False

    # Carga la librería de gráficos de Windows (GDI32)
    gdi32 = ctypes.WinDLL('gdi32')
    
    # Definimos los tipos de datos necesarios para la API de Windows
    FR_PRIVATE = 0x10
    ruta_abs = os.path.abspath(ruta_fuente)
    
    # Llamamos a la función AddFontResourceExW de Windows
    # Esto registra la fuente en la sesión actual del usuario sin instalarla permanentemente
    num_fuentes_cargadas = gdi32.AddFontResourceExW(
        wintypes.LPCWSTR(ruta_abs), 
        wintypes.DWORD(FR_PRIVATE), 
        0
    )
    
    if num_fuentes_cargadas > 0:
        print(f"Fuente cargada exitosamente: {ruta_fuente}")
        return True
    else:
        print("No se pudo cargar la fuente.")
        return False