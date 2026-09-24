import os
import sys
import yt_dlp
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading

# Detectar ruta en tiempo de ejecución (PyInstaller --onefile extrae en _MEIPASS)
if getattr(sys, "frozen", False):
    MEIPASS = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    MEIPASS = os.path.dirname(__file__)

# Ruta a ffmpeg.exe
FFMPEG_PATH = os.path.join(MEIPASS, "ffmpeg", "bin", "ffmpeg.exe")

# Variables
yt_url = ""
carpetas = ['music', 'video']
ruta_base = os.path.join(os.getcwd(), 'descargas')

# Crear carpetas necesarias
for carpeta in carpetas:
    ruta_completa = os.path.join(ruta_base, carpeta)
    os.makedirs(ruta_completa, exist_ok=True)
    print(f"Carpeta '{ruta_completa}' creada o ya existente.")

# Funciones de descarga
def get_url():
    global yt_url
    yt_url = Entry_URL.get().strip()
    if not yt_url:
        messagebox.showwarning("URL vacía", "Introduce una URL valida.")
    else:
        print("URL introducida:", yt_url)

def _check_url_or_alert():
    if not yt_url:
        messagebox.showwarning("URL vacía", "Introduce la URL antes de descargar.")
        return False
    return True

# Hook para actualizar la barra de progreso desde yt_dlp
def progress_hook(d):
    # d tiene keys como 'status', 'downloaded_bytes', 'total_bytes' o 'total_bytes_estimate'
    try:
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = downloaded / total * 100
                # root puede no existir al definir la función, pero sí al ejecutarla
                root.after(0, progress_var.set, percent)
        elif d.get('status') == 'finished':
            # descarga completada -> marcar 100%
            root.after(0, progress_var.set, 100)
    except Exception as e:
        # evitar que el hook rompa la descarga por excepción en UI
        print("progress_hook error:", e)

def Descargar_Video_1080p():
    if not _check_url_or_alert():
        return
    # reiniciar barra
    root.after(0, progress_var.set, 0)
    ydl_opts = {
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        'outtmpl': os.path.join(ruta_base, 'video', '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'writethumbnail': False,
        'embedmetadata': False,
        'socket_timeout': 10,
        'retries': 5,
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        messagebox.showinfo("Completado", "Descarga de video 1080p completada.")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la descarga: {e}")
        print("Error:", e)
    progress_var.set(ydl.download_with_info_file.progress) # Actualizar la barra de progreso


def Descargar_Video_720p():
    if not _check_url_or_alert():
        return
    root.after(0, progress_var.set, 0)
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        'outtmpl': os.path.join(ruta_base, 'video', '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'writethumbnail': False,
        'embedmetadata': False,
        'socket_timeout': 10,
        'retries': 5,
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        messagebox.showinfo("Completado", "Descarga de video 720p completada.")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la descarga: {e}")
        print("Error:", e)

def Descargar_Musica():
    if not _check_url_or_alert():
        return
    root.after(0, progress_var.set, 0)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(ruta_base, 'music', '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        messagebox.showinfo("Completado", "Descarga de música completada.")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la descarga: {e}")
        print("Error:", e)

# UI
root = tk.Tk()
root.title("YT Downloader")

label_Menu = tk.LabelFrame(root, text="Menu Principal", background="lemon chiffon")
label_Menu.config(height=600, width=400)
label_Menu.pack(padx=10, pady=10)

Label_Text = tk.Label(label_Menu, text="Descarga videos y música de YouTube",
                    height=3, width=35, background="gold")
Label_Text.pack(pady=10)

Label_URL = tk.Label(label_Menu, text="Introduce La URL")
Label_URL.pack(pady=5)
Entry_URL = tk.Entry(label_Menu, width=40)
Entry_URL.pack(pady=5)

Button_Intro_URL = tk.Button(label_Menu, text="Introducir URL", command=get_url)
Button_Intro_URL.pack(pady=5)

#barra de descarga para saber el progreso de la descarga

# Crear una variable de control (DoubleVar) antes de crear la barra de progreso.
# La opción 'variable' del Progressbar debe recibir esta variable, no un atributo
# de 'bar' que aún no existe.
progress_var = tk.DoubleVar()

# Usar 'ttk.Progressbar' (importado como 'ttk') y asociar la variable de control.
# maximum=100 indica el valor máximo de la barra; se puede actualizar con
# progress_var.set(valor) desde las descargas para reflejar el progreso.
bar = ttk.Progressbar(label_Menu, variable=progress_var, maximum=100)
bar.pack(pady=10, fill=tk.X, padx=20)

# Inicializar el valor a 0.
progress_var.set(0)

# Ocultar la barra inicialmente; mostrarla con bar.pack() cuando empiece la descarga.
bar.pack()  # Ocultar la barra inicialmente

# Las descargas se lanzan en hilos para no bloquear la UI
Button_Descargar_Video_1080p = tk.Button(
    label_Menu, text="Video 1080p",
    command=lambda: threading.Thread(target=Descargar_Video_1080p, daemon=True).start()
)
Button_Descargar_Video_1080p.pack(pady=6)

Button_Descargar_Video_720p = tk.Button(
    label_Menu, text="Video 720p",
    command=lambda: threading.Thread(target=Descargar_Video_720p, daemon=True).start()
)
Button_Descargar_Video_720p.pack(pady=6)

Button_Musica = tk.Button(
    label_Menu, text="Musica",
    command=lambda: threading.Thread(target=Descargar_Musica, daemon=True).start()
)
Button_Musica.pack(pady=5)

Label_By = tk.Label(label_Menu, text="By Albert", background="lemon chiffon")
Label_By.pack(pady=10)

def Salir():
    root.destroy()

Button_Salir = tk.Button(label_Menu, text="Salir", command=Salir)
Button_Salir.pack(pady=10)

root.mainloop()
print("aqui termina")
