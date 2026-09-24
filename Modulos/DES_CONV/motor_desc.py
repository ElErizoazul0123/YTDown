import os
import sys
import threading
import yt_dlp
from tkinter import messagebox
import Modulos.UI.util_imagenes as util_imagenes

# ==========================================================
# ZONA 1: CONFIGURACIÓN Y RUTAS (se ejecuta al importar)
# ==========================================================
Url = ""
carpetas = ["music", "video"]

if getattr(sys, "frozen", False):
    RUTA_BASE = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    # motor_desc.py vive en Modulos/DES_CONV/ → subimos 3 niveles a la raíz
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ruta_base = os.path.join(RUTA_BASE, 'descargas')
FFMPEG_PATH = os.path.join(RUTA_BASE, "ffmpeg", "bin")

# ffmpeg en el PATH del proceso: yt-dlp lo encontrará siempre
os.environ["PATH"] = FFMPEG_PATH + os.pathsep + os.environ.get("PATH", "")

print(f"[DEBUG] Ruta ffmpeg: {FFMPEG_PATH}")
print(f"[DEBUG] ffmpeg.exe existe: {os.path.isfile(os.path.join(FFMPEG_PATH, 'ffmpeg.exe'))}")
print(f"[DEBUG] ffprobe.exe existe: {os.path.isfile(os.path.join(FFMPEG_PATH, 'ffprobe.exe'))}")

for carpeta in carpetas:
    ruta_completa = os.path.join(ruta_base, carpeta)
    os.makedirs(ruta_completa, exist_ok=True)
    print(f"Carpeta '{ruta_completa}' creada o ya existente.")


# ==========================================================
# ZONA 2: AYUDANTES INTERNOS (la ventana NO los llama)
# ==========================================================
def _check_url_or_alert():
    if not Url:
        messagebox.showwarning("URL vacía", "Introduce la URL antes de descargar.")
        return False
    return True


def _hook_progreso(actualizador):
    """Devuelve un hook de yt-dlp que llama a actualizador(porcentaje)."""
    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            if total:
                actualizador(d.get('downloaded_bytes', 0) / total * 100)
        elif d['status'] == 'finished':
            actualizador(100)
    return hook


def _lanzar_en_hilo(ydl_opts, on_progreso=None, al_terminar=None):
    """Ejecuta la descarga en un hilo secundario para no congelar la UI."""
    if on_progreso:
        ydl_opts['progress_hooks'] = [_hook_progreso(on_progreso)]

    def worker():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([Url])
            if al_terminar:
                al_terminar("ok", "")
        except Exception as e:
            print("Error:", e)
            if al_terminar:
                al_terminar("error", str(e))

    threading.Thread(target=worker, daemon=True).start()


# ==========================================================
# ZONA 3: FUNCIONES PÚBLICAS (la ventana SÍ las llama)
# ==========================================================
def get_url(entry_widget):
    global Url
    Url = entry_widget.get().strip()
    print("URL obtenida:", Url)
    if not Url:
        messagebox.showwarning("URL vacía", "Introduce una URL valida.")


def Descargar_Video_1080p(on_progreso=None, al_terminar=None):
    if not _check_url_or_alert():
        return
    ydl_opts = {
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        'outtmpl': os.path.join(ruta_base, 'video', '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'writethumbnail': False,
        'embedmetadata': False,
        'socket_timeout': 10,
        'retries': 5,
        'ffmpeg_location': FFMPEG_PATH,
    }
    _lanzar_en_hilo(ydl_opts, on_progreso, al_terminar)


def Descargar_Video_720p(on_progreso=None, al_terminar=None):
    if not _check_url_or_alert():
        return
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        'outtmpl': os.path.join(ruta_base, 'video', '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'writethumbnail': False,
        'embedmetadata': False,
        'socket_timeout': 10,
        'retries': 5,
        'ffmpeg_location': FFMPEG_PATH,
    }
    _lanzar_en_hilo(ydl_opts, on_progreso, al_terminar)


def Descargar_Musica(on_progreso=None, al_terminar=None):
    if not _check_url_or_alert():
        return
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(ruta_base, 'music', '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': FFMPEG_PATH,
    }
    _lanzar_en_hilo(ydl_opts, on_progreso, al_terminar)


def Descargar_Musica_Caratula(on_progreso=None, al_terminar=None):
    if not _check_url_or_alert():
        return
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(ruta_base, 'music', '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            {'key': 'EmbedThumbnail'},
        ],
        'ffmpeg_location': FFMPEG_PATH,
    }
    _lanzar_en_hilo(ydl_opts, on_progreso, al_terminar)


def process_boton_descarga(entry_widget):
    Url_local = entry_widget.get().strip()
    if not Url_local:
        messagebox.showwarning("URL vacía", "Introduce una URL válida.")
        return None, None

    global Url
    Url = Url_local

    imagen_activa = util_imagenes.caratula_imagen(Url_local, (300, 200))
    return imagen_activa, Url_local