#explicacion de centrar ventana (ventana) es la ventana que se quiere centrar (ancho) es el ancho deseado de la ventana (alto) es el alto deseado de la ventana
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    #dimensiones es ancho x alto + posicion x + posicion y
    return ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
