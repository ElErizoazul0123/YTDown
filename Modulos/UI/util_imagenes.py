from PIL import ImageTk, Image
import requests
import yt_dlp
from io import BytesIO

imagen_main = None



def cargar_imagen(ruta, tamaño):
        
        imagen_main = Image.open(ruta).resize(tamaño, Image.LANCZOS)

        return ImageTk.PhotoImage(imagen_main)

def carga_imagen_btn(url, tamaño):
    img = caratula_imagen(url, tamaño)
    if img:
        imagen_main = ImageTk.PhotoImage(img)
        return imagen_main
    else:
            return None

def caratula_imagen(url, tamaño):
    # 1. Configuración mínima para que sea rápido
    ydl_opts = {'skip_download': True, 'quiet': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos la info sin bajar el video
            info = ydl.extract_info(url, download=False)
            
            # Buscamos la URL de la imagen. 
            # Usamos [-1] porque YouTube suele poner la de mayor calidad al final.
            caratula_url = info['thumbnails'][-1]['url']
        
        # 2. Bajamos la imagen de internet
        respuesta = requests.get(caratula_url, timeout=5)
        
        # 3. La convertimos de "bytes" a "imagen de Pillow"
        # BytesIO(respuesta.content) convierte los datos crudos en un "archivo virtual"
        imagen_pil = Image.open(BytesIO(respuesta.content))
        
        # 4. Redimensionamos con LANCZOS (el mejor filtro para fotos)
        return imagen_pil.resize(tamaño, Image.LANCZOS)

    except Exception as e:
        print(f"Error: {e}")
        return None