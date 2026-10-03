# 🎵 YTDown

**Descargador de música y videos de YouTube con interfaz gráfica moderna.**

YTDown es una aplicación de escritorio desarrollada en Python que permite descargar música en MP3 (con o sin carátula) y videos en calidad 720p o 1080p desde YouTube. Cuenta con una interfaz intuitiva.

> 🚧 **Versión actual:** Beta 0.2

---

## ✨ Características

- 🎵 **Modo Música**
  - Descarga en MP3 a 192 kbps
  - Opción de incluir carátula incrustada en el archivo
- 🎬 **Modo Video**
  - Descarga en 1080p (MP4)
  - Descarga en 720p (MP4)
- 📋 **Cola de descargas** con estado individual por tarea
- 🖼️ **Vista previa de carátula** antes de descargar

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python 3.11+** | Lenguaje principal |
| **Tkinter** | Interfaz gráfica |
| **yt-dlp** | Motor de descargas |
| **FFmpeg** | Conversión a MP3 y unión de video+audio |
| **Pillow (PIL)** | Manejo de imágenes y carátulas |
| **Font Awesome 7 Free** | Iconos de la interfaz |

---

## 📋 Requisitos

- **Python 3.11 o superior**
- **FFmpeg** (incluido en la carpeta `ffmpeg/` del proyecto)
- **Windows 10/11** (probado en este sistema; debería funcionar en Linux/macOS con ajustes mínimos)

Uso educativo y personal. Respeta los términos de YouTube y los derechos de autor.