import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import webbrowser
from PIL import Image, ImageTk
from config import CONS_COLOR_BARRA_SUPERIOR, CONS_COLOR_BARRA_IZQUIERDA, CONS_COLOR_BARRA_DERECHA, CONS_COLOR_BOTON_ACTUAL, CONS_COLOR_BOTON_DESACTIVADO
import Modulos.UI.util_imagenes as util_imagenes
import Modulos.UI.util_ventanas as util_ventanas
import Modulos.UI.util_fuentes as util_fuentes
import Modulos.DES_CONV.motor_desc as MotorDescarga


global media
media = None

class ventana_principal(tk.Tk):

    def __init__(self):
        """Inicialización de la ventana principal"""
        super().__init__()
        
        self.logo = util_imagenes.cargar_imagen("Recursos/imagenes/arch-linux.png", (100, 100))
        ruta_fuent = r"Recursos\fuentes\Font Awesome 7 Free-Regular-400.otf"
        util_fuentes.cargar_fuente_personalizada(ruta_fuent)

        self.configurar_ventana()
        self.paneles()
        self.menu_lateral()
        self.cuerpo_principal()
        self.elementos_barra_superior()
#        self.elementos_menu_lateral()
        self.elementos_cuerpo_principal()
        self.prev_info_descarga()
        self.cola_de_descarga()

    # ================================================================
    # CONFIGURACIÓN DE LA VENTANA
    # ================================================================
    def configurar_ventana(self):
        """Configura título, icono, tamaño y centrado"""
        self.title("YTDown")
        self.iconbitmap("Recursos/imagenes/arch-linux.ico")
        w, h = 1024, 600
        util_ventanas.centrar_ventana(self, w, h)
        self.resizable(False, False)

    # ================================================================
    # PANELES PRINCIPALES
    # ================================================================
    def paneles(self):
        """Panel superior (barra de título)"""
        self.barra_superior = tk.Frame(self, bg=CONS_COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side="top", fill="both")

    def menu_lateral(self):
        """Panel izquierdo (menú lateral) con información y enlaces"""
        self.menu_lateral = tk.Frame(self, bg=CONS_COLOR_BARRA_IZQUIERDA, width=200)
    #    self.menu_lateral.pack(side="left", fill="both", expand=False)
        
        # Título del menú
        tk.Label(
            self.menu_lateral, 
            text="YTDown",
            bg=CONS_COLOR_BARRA_IZQUIERDA, 
            fg="white", 
            font=("Roboto", 18, "bold")
        ).pack(side="top", pady=20)
        
        # Separador
        tk.Frame(self.menu_lateral, bg="white", height=1).pack(side="top", fill="x", padx=10)
        
        # Label de versión
        tk.Label(
            self.menu_lateral,
            text="Versión Beta 0.1",
            bg=CONS_COLOR_BARRA_IZQUIERDA,
            fg="#cccccc",
            font=("Roboto", 10)
        ).pack(side="top", pady=10)
        
        # Espacio flexible
        tk.Frame(self.menu_lateral, bg=CONS_COLOR_BARRA_IZQUIERDA).pack(side="top", expand=True)
        
        # Label de URL con enlace a GitHub
        url_label = tk.Label(
            self.menu_lateral,
            text="GitHub",
            bg=CONS_COLOR_BARRA_IZQUIERDA,
            fg="#4da6ff",
            font=("Roboto", 10, "underline"),
            cursor="hand2"
        )
        url_label.pack(side="top", pady=5)
        url_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/ElErizoazul0123/YTDown"))
        
        # Separador
        tk.Frame(self.menu_lateral, bg="white", height=1).pack(side="top", fill="x", padx=10, pady=10)
        
        # Firma JAcode
        tk.Label(
            self.menu_lateral,
            text="Desarrollado por",
            bg=CONS_COLOR_BARRA_IZQUIERDA,
            fg="#999999",
            font=("Roboto", 9)
        ).pack(side="top")
        
        firma_label = tk.Label(
            self.menu_lateral,
            text="JAcode",
            bg=CONS_COLOR_BARRA_IZQUIERDA,
            fg="white",
            font=("Roboto", 14, "bold")
        )
        firma_label.pack(side="top", pady=5)

    def cuerpo_principal(self):
        """Panel derecho (área principal de contenido)"""
        self.cuerpo_principal = tk.Frame(self, bg=CONS_COLOR_BARRA_DERECHA, width=200)
        self.cuerpo_principal.pack(side="right", fill="both", expand=True)

    # ================================================================
    # ELEMENTOS DE LA BARRA SUPERIOR
    # ================================================================
    def elementos_barra_superior(self): 
        """Botón de configuración y título"""
        font_awesome = font.Font(family="FontAwesome", size=16)

        self.button_config = tk.Button(self.barra_superior, text="\u2699", font=font_awesome, 
                                       bg=CONS_COLOR_BARRA_SUPERIOR, command=self.toggle_menu, 
                                       fg="white", borderwidth=0, 
                                       activebackground=CONS_COLOR_BARRA_SUPERIOR, 
                                       activeforeground="white")
        self.button_config.pack(side="left", padx=10)

        self.label_titulo = tk.Label(self.barra_superior, text=" ", 
                                     bg=CONS_COLOR_BARRA_SUPERIOR, fg="white", 
                                     font=("Roboto", 16, "bold"))
        self.label_titulo.pack(side="left", padx=10)

    def elementos_menu_lateral(self):
        """Elementos del menú lateral (pendiente de implementar)"""
        pass

    # ================================================================
    # ELEMENTOS DEL CUERPO PRINCIPAL
    # ================================================================
    def elementos_cuerpo_principal(self):
        """Pestañas Music/Video y contenedores de mitades"""
        font_awesome = font.Font(family="FontAwesome", size=16)

        # Contenedor para pestañas de modo
        self.cont_buttons_media = tk.Frame(self.cuerpo_principal) 
        self.cont_buttons_media.pack(side="top", fill="both")

        # Pestaña MUSIC
        self.boton_menu_music = tk.Button(
            self.cont_buttons_media, bg=CONS_COLOR_BOTON_ACTUAL, fg="white",
            font=font_awesome, text="Music", borderwidth=0,
            command=lambda: self.cambiar_modo("music"))
        self.boton_menu_music.pack(side="left", expand=True, fill="both")

        # Pestaña VIDEO
        self.boton_menu_video = tk.Button(
            self.cont_buttons_media, bg=CONS_COLOR_BOTON_DESACTIVADO, fg="white",
            font=font_awesome, text="Video", borderwidth=0,
            command=lambda: self.cambiar_modo("video"))
        self.boton_menu_video.pack(side="right", expand=True, fill="both")

        # Mitad izquierda (controles de descarga)
        self.cont_mitad_izquierda = tk.Frame(self.cuerpo_principal, bg=CONS_COLOR_BARRA_DERECHA)
        self.cont_mitad_izquierda.pack(side="left", fill="both", expand=True)
        
        # Mitad derecha (cola de descargas)
        self.cont_mitad_derecha = tk.Frame(self.cuerpo_principal)
        self.cont_mitad_derecha.pack(side="right", fill="both", expand=True)

    def prev_info_descarga(self):
        """Sección izquierda: carátula, URL, botones de descarga y barra de progreso"""
        etiqueta_cancion = tk.Label(self.cont_mitad_izquierda, text="Cancion:", 
                                    bg=CONS_COLOR_BARRA_DERECHA, fg="white", 
                                    font=("Roboto", 14))
        etiqueta_cancion.pack(side="top", pady=10)

        # Carátula del video/música
        self.etiqueta_caratula = tk.Label(self.cont_mitad_izquierda, image=None, 
                                          bg=CONS_COLOR_BARRA_DERECHA)
        self.etiqueta_caratula.pack()

        # Campo de entrada de URL
        self.entry_url_label = tk.Label(self.cont_mitad_izquierda, text="Introduce la URL:", 
                                        bg=CONS_COLOR_BARRA_DERECHA, fg="white", 
                                        font=("Roboto", 12, "bold"))
        self.entry_url_label.pack(side="top", pady=5)

        self.entry_url = tk.Entry(self.cont_mitad_izquierda, width=70)
        self.entry_url.pack(side="top")

        # Contenedor para botones del modo activo
        self.cont_botones_modo = tk.Frame(self.cont_mitad_izquierda, bg=CONS_COLOR_BARRA_DERECHA)
        self.cont_botones_modo.pack(side="top", pady=5)

        # Frame MÚSICA (visible al inicio)
        self.cont_botones_music = tk.Frame(self.cont_botones_modo, bg=CONS_COLOR_BARRA_DERECHA)
        self.cont_botones_music.pack(side="top")

        self.boton_descargar_music_carat = tk.Button(
            self.cont_botones_music, text="Descargar Música con Carátula", relief="flat",
            bg=CONS_COLOR_BARRA_IZQUIERDA, fg="white", font=("Roboto", 12, "bold"),
            command=lambda: self.disparar_proceso_descarga("music_caratula"))
        self.boton_descargar_music_carat.pack(side="top", pady=5)

        self.boton_descargar_music_sin_carat = tk.Button(
            self.cont_botones_music, text="Descargar Música", relief="flat",
            bg=CONS_COLOR_BARRA_IZQUIERDA, fg="white", font=("Roboto", 12, "bold"),
            command=lambda: self.disparar_proceso_descarga("music"))
        self.boton_descargar_music_sin_carat.pack(side="top", pady=5)

        # Frame VIDEO (oculto al inicio)
        self.cont_botones_video = tk.Frame(self.cont_botones_modo, bg=CONS_COLOR_BARRA_DERECHA)

        self.boton_descargar_video_1080 = tk.Button(
            self.cont_botones_video, text="Descargar Video 1080p", relief="flat",
            bg=CONS_COLOR_BARRA_IZQUIERDA, fg="white", font=("Roboto", 12, "bold"),
            command=lambda: self.disparar_proceso_descarga("video_1080"))
        self.boton_descargar_video_1080.pack(side="top", pady=5)

        self.boton_descargar_video_720 = tk.Button(
            self.cont_botones_video, text="Descargar Video 720p", relief="flat",
            bg=CONS_COLOR_BARRA_IZQUIERDA, fg="white", font=("Roboto", 12, "bold"),
            command=lambda: self.disparar_proceso_descarga("video_720"))
        self.boton_descargar_video_720.pack(side="top", pady=5)

        # Barra de progreso
        self.barra_progreso = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(self.cont_mitad_izquierda, 
                                          variable=self.barra_progreso, maximum=100)
        self.progressbar.pack(side="top", pady=10, fill="x", padx=20)
        self.barra_progreso.set(0)

    # ================================================================
    # COLA DE DESCARGAS (PANEL GRIS)
    # ================================================================
    def cola_de_descarga(self):
        """Panel derecho: lista visual de tareas en cola"""
        self.cola_de_descarga = tk.Frame(self.cont_mitad_derecha, bg="gray", height=100)
        self.cola_de_descarga.pack(side="top", fill="both", expand=True)

        # Título del panel
        tk.Label(self.cola_de_descarga, text="Cola de descargas",
                 bg="gray", fg="white", font=("Roboto", 12, "bold")).pack(side="top", pady=5)

        # Lista visual de tareas
        self.lista_cola = tk.Listbox(self.cola_de_descarga, bg="#2b2b2b", fg="white",
                                     relief="flat", selectbackground="#555")
        self.lista_cola.pack(side="top", fill="both", expand=True, padx=8, pady=5)

        # Estado interno de tareas
        self.tareas = {}
        self._contador_tareas = 0

    # ================================================================
    # GESTIÓN DE TAREAS (NUEVOS MÉTODOS)
    # ================================================================
    def agregar_tarea(self, nombre):
        """Agrega una tarea a la cola y retorna su ID"""
        self._contador_tareas += 1
        tid = self._contador_tareas
        self.tareas[tid] = {"nombre": nombre, "estado": "⏳ Descargando..."}
        self._refrescar_cola()
        return tid

    def _cerrar_tarea(self, tid, estado, detalle=""):
        """Marca una tarea como completada o con error"""
        if tid not in self.tareas:
            return
        if estado == "ok":
            self.tareas[tid]["estado"] = "✅ Completada"
            messagebox.showinfo("Completado", "Descarga finalizada.")
        else:
            self.tareas[tid]["estado"] = "❌ Error"
            messagebox.showerror("Error", f"Error durante la descarga:\n{detalle}")
        self._refrescar_cola()

    def _refrescar_cola(self):
        """Actualiza la lista visual de tareas"""
        self.lista_cola.delete(0, "end")
        for tid, t in self.tareas.items():
            texto = f"{t['nombre'][:38]}  |  {t['estado']}"
            self.lista_cola.insert("end", texto)

    # ================================================================
    # INTERACCIÓN DE USUARIO
    # ================================================================
    def toggle_menu(self):
        """Muestra/oculta el menú lateral"""
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side="left", fill="both", expand=False)

    def cambiar_modo(self, modo):
        """Alterna entre la interfaz de música y video"""
        self.modo_actual = modo

        if modo == "music":
            self.boton_menu_music.config(bg=CONS_COLOR_BOTON_ACTUAL)
            self.boton_menu_video.config(bg=CONS_COLOR_BOTON_DESACTIVADO)
            self.cont_botones_video.pack_forget()
            self.cont_botones_music.pack(side="top")

        elif modo == "video":
            self.boton_menu_video.config(bg=CONS_COLOR_BOTON_ACTUAL)
            self.boton_menu_music.config(bg=CONS_COLOR_BOTON_DESACTIVADO)
            self.cont_botones_music.pack_forget()
            self.cont_botones_video.pack(side="top")

    # ================================================================
    # LÓGICA DE DESCARGA
    # ================================================================
    def disparar_proceso_descarga(self, tipo_media):
        """Maneja el clic en cualquier botón de descarga"""
        # 1. Obtener URL e imagen del motor
        imagen_pil, url_obtenida = MotorDescarga.process_boton_descarga(self.entry_url)

        # Si no hay URL válida, process_boton_descarga retorna (None, None)
        if imagen_pil is None:
            return

        # 2. Mostrar carátula
        self.foto_lista = ImageTk.PhotoImage(imagen_pil)
        self.etiqueta_caratula.config(image=self.foto_lista)
        self.etiqueta_caratula.image = self.foto_lista
        print(f"Éxito: Mostrando carátula de {url_obtenida}")

        # 3. Registrar tarea en la cola y lanzar descarga
        self.barra_progreso.set(0)
        tid = self.agregar_tarea(url_obtenida)
        
        # Callbacks para progreso y finalización (puente hilo→UI)
        on_prog = lambda p: self.after(0, self.barra_progreso.set, p)
        on_fin = lambda e, d: self.after(0, self._cerrar_tarea, tid, e, d)

        # 4. Lanzar descarga según el tipo
        if tipo_media == "music":
            MotorDescarga.Descargar_Musica(on_prog, on_fin)
        elif tipo_media == "music_caratula":
            MotorDescarga.Descargar_Musica_Caratula(on_prog, on_fin)
        elif tipo_media == "video_1080":
            MotorDescarga.Descargar_Video_1080p(on_prog, on_fin)
        elif tipo_media == "video_720":
            MotorDescarga.Descargar_Video_720p(on_prog, on_fin)