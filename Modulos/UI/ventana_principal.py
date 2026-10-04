import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import webbrowser
from PIL import Image, ImageTk
from tkinter import filedialog
from config import (P)
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
        util_fuentes.cargar_fuente_personalizada(r"Recursos\fuentes\Font Awesome 7 Free-Solid-900.otf")
        util_fuentes.cargar_fuente_personalizada(r"Recursos\fuentes\Font Awesome 7 Free-Regular-400.otf")
        util_fuentes.cargar_fuente_personalizada(r"Recursos\fuentes\Font Awesome 7 Brands-Regular-400.otf")

        self._aplicar_estilos_ttk()
        self.configurar_ventana()
        self.paneles()
        self.menu_lateral()
        self.cuerpo_principal()
        self.elementos_barra_superior()
        self.elementos_cuerpo_principal()
        self.prev_info_descarga()
        self.cola_de_descarga()

    # ================================================================
    # ESTILOS TTK GLOBALES (progressbar, scrollbar, listbox)
    # ================================================================
    def _aplicar_estilos_ttk(self):
        """Aplica el tema morado a todos los widgets ttk."""
        s = ttk.Style(self)
        s.theme_use("clam")

        # Progressbar
        s.configure(
            "Purple.Horizontal.TProgressbar",
            troughcolor=P["bar_trough"],
            background=P["bar_fill"],
            bordercolor=P["border"],
            lightcolor=P["accent_light"],
            darkcolor=P["accent_dim"],
            thickness=8,
        )

        # Scrollbar (para la listbox de la cola)
        s.configure(
            "Purple.Vertical.TScrollbar",
            troughcolor=P["bg_deep"],
            background=P["accent_dim"],
            bordercolor=P["border"],
            arrowcolor=P["fg_secondary"],
        )

    # ================================================================
    # CONFIGURACIÓN DE LA VENTANA
    # ================================================================
    def configurar_ventana(self):
        """Configura título, icono, tamaño y centrado"""
        self.title("YTDown")
        self.iconbitmap("Recursos/imagenes/arch-linux.ico")
        self.configure(bg=P["bg_dark"])
        w, h = 1024, 600
        util_ventanas.centrar_ventana(self, w, h)
        self.resizable(False, False)

    # ================================================================
    # PANELES PRINCIPALES
    # ================================================================
    def paneles(self):
        """Panel superior (barra de título)"""
        self.barra_superior = tk.Frame(self, bg=P["bg_panel"], height=50)
        self.barra_superior.pack(side="top", fill="both")

        # Franja de acento debajo de la barra superior
        tk.Frame(self, bg=P["separator"], height=2).pack(side="top", fill="x")

    def menu_lateral(self):
        """Panel izquierdo (menú lateral) con información y enlaces"""
        self.menu_lateral = tk.Frame(self, bg=P["bg_panel"], width=200)

        # Franja de acento vertical en el borde derecho del menú
        self._franja_lateral = tk.Frame(self.menu_lateral, bg=P["accent"], width=3)
        self._franja_lateral.pack(side="right", fill="y")

        # Título del menú
        tk.Label(
            self.menu_lateral,
            text="YTDown",
            bg=P["bg_panel"],
            fg=P["accent_light"],
            font=("Roboto", 18, "bold")
        ).pack(side="top", pady=20)

        # Separador
        tk.Frame(self.menu_lateral, bg=P["separator"], height=1).pack(
            side="top", fill="x", padx=10)

        # Label de versión
        tk.Label(
            self.menu_lateral,
            text="Versión Beta 0.3",
            bg=P["bg_panel"],
            fg=P["fg_muted"],
            font=("Roboto", 10)
        ).pack(side="top", pady=10)

        # Botón para cambiar la ruta de descarga
        boton_cambiar_ruta = tk.Button(
            self.menu_lateral,
            text="Cambiar ruta de descarga",
            command=self.cambiar_carpeta_descargas,
            bg=P["accent_dim"],
            fg=P["fg_primary"],
            relief="flat",
            cursor="hand2",
            activebackground=P["accent"],
            activeforeground=P["fg_primary"],
            font=("Roboto", 9),
            padx=6, pady=4,
        )
        boton_cambiar_ruta.pack(side="top", pady=5, padx=12, fill="x")

        # Espacio flexible
        tk.Frame(self.menu_lateral, bg=P["bg_panel"]).pack(side="top", expand=True)

        # Label GitHub
        url_label = tk.Label(
            self.menu_lateral,
            text="GitHub",
            bg=P["bg_panel"],
            fg=P["accent_light"],
            font=("Roboto", 10, "underline"),
            cursor="hand2"
        )
        url_label.pack(side="top", pady=5)
        url_label.bind("<Button-1>", lambda e: webbrowser.open(
            "https://github.com/ElErizoazul0123/YTDown"))

        # Separador
        tk.Frame(self.menu_lateral, bg=P["separator"], height=1).pack(
            side="top", fill="x", padx=10, pady=10)

        # Firma
        tk.Label(
            self.menu_lateral,
            text="Desarrollado por",
            bg=P["bg_panel"],
            fg=P["fg_muted"],
            font=("Roboto", 9)
        ).pack(side="top")

        firma_label = tk.Label(
            self.menu_lateral,
            text="JAcode",
            bg=P["bg_panel"],
            fg=P["fg_primary"],
            font=("Roboto", 14, "bold")
        )
        firma_label.pack(side="top", pady=(2, 14))

    def cuerpo_principal(self):
        """Panel derecho (área principal de contenido)"""
        self.cuerpo_principal = tk.Frame(self, bg=P["bg_dark"])
        self.cuerpo_principal.pack(side="right", fill="both", expand=True)

    # ================================================================
    # ELEMENTOS DE LA BARRA SUPERIOR
    # ================================================================
    def elementos_barra_superior(self):
        """Botón de configuración y título"""
        font_awesome = font.Font(family="Font Awesome 7 Free Solid", size=16)

        self.button_config = tk.Button(
            self.barra_superior,
            text="\uf013",
            font=font_awesome,
            bg=P["bg_panel"],
            command=self.toggle_menu,
            fg=P["fg_secondary"],
            borderwidth=0,
            activebackground=P["bg_panel"],
            activeforeground=P["accent_light"],
            cursor="hand2",
        )
        self.button_config.pack(side="left", padx=10)

        self.label_titulo = tk.Label(
            self.barra_superior,
            text=" ",
            bg=P["bg_panel"],
            fg=P["fg_primary"],
            font=("Roboto", 16, "bold")
        )
        self.label_titulo.pack(side="left", padx=10)

    def elementos_menu_lateral(self):
        """Elementos del menú lateral (pendiente de implementar)"""
        pass

    # ================================================================
    # ELEMENTOS DEL CUERPO PRINCIPAL
    # ================================================================
    def elementos_cuerpo_principal(self):
        """Pestañas Music/Video y contenedores de mitades"""
        font_awesome = font.Font(family="Font Awesome 7 Free Solid", size=16)

        # Contenedor para pestañas de modo
        self.cont_buttons_media = tk.Frame(self.cuerpo_principal, bg=P["bg_dark"])
        self.cont_buttons_media.pack(side="top", fill="both")

        # Pestaña MUSIC — activa
        self.boton_menu_music = tk.Button(
            self.cont_buttons_media,
            bg=P["accent"],
            fg=P["fg_primary"],
            font=font_awesome,
            text="Music " + "\uf001",
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            activebackground=P["accent_glow"],
            activeforeground=P["fg_primary"],
            pady=8,
            command=lambda: self.cambiar_modo("music"),
        )
        self.boton_menu_music.pack(side="left", expand=True, fill="both")

        # Pestaña VIDEO — inactiva
        self.boton_menu_video = tk.Button(
            self.cont_buttons_media,
            bg=P["accent_dim"],
            fg=P["fg_secondary"],
            font=font_awesome,
            text="Video " + "\uf03d",
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            activebackground=P["accent_glow"],
            activeforeground=P["fg_primary"],
            pady=8,
            command=lambda: self.cambiar_modo("video"),
        )
        self.boton_menu_video.pack(side="right", expand=True, fill="both")

        # Línea divisora entre pestañas y contenido
        tk.Frame(self.cuerpo_principal, bg=P["separator"], height=2).pack(
            side="top", fill="x")

        # Mitad izquierda (controles de descarga)
        self.cont_mitad_izquierda = tk.Frame(self.cuerpo_principal, bg=P["bg_card"])
        self.cont_mitad_izquierda.pack(side="left", fill="both", expand=True)

        # Línea separadora vertical
        tk.Frame(self.cuerpo_principal, bg=P["border"], width=2).pack(
            side="left", fill="y")

        # Mitad derecha (cola de descargas)
        self.cont_mitad_derecha = tk.Frame(self.cuerpo_principal, bg=P["bg_queue"])
        self.cont_mitad_derecha.pack(side="right", fill="both", expand=True)

    def prev_info_descarga(self):
        """Sección izquierda: carátula, URL, botones de descarga y barra de progreso"""
        etiqueta_media = tk.Label(
            self.cont_mitad_izquierda,
            text="Media",
            bg=P["bg_card"],
            fg=P["accent_light"],
            font=("Roboto", 13, "bold")
        )
        etiqueta_media.pack(side="top", pady=(14, 6))

        # Carátula del video/música
        self.etiqueta_caratula = tk.Label(
            self.cont_mitad_izquierda,
            image=None,
            bg=P["bg_card"],
        )
        self.etiqueta_caratula.pack()

        # Campo de entrada de URL
        self.entry_url_label = tk.Label(
            self.cont_mitad_izquierda,
            text="Introduce la URL:",
            bg=P["bg_card"],
            fg=P["fg_secondary"],
            font=("Roboto", 12, "bold")
        )
        self.entry_url_label.pack(side="top", pady=(10, 2))

        self.entry_url = tk.Entry(
            self.cont_mitad_izquierda,
            width=50,
            bg=P["bg_deep"],
            fg=P["fg_primary"],
            insertbackground=P["accent_light"],
            relief="flat",
            font=("Roboto", 10),
            highlightthickness=1,
            highlightcolor=P["accent"],
            highlightbackground=P["border"],
        )
        self.entry_url.pack(side="top", ipady=5, padx=20)

        # Contenedor para botones del modo activo
        self.cont_botones_modo = tk.Frame(self.cont_mitad_izquierda, bg=P["bg_card"])
        self.cont_botones_modo.pack(side="top", pady=10)

        # Estilo compartido para botones de descarga
        _btn_kw = dict(
            relief="flat",
            bg=P["accent_dim"],
            fg=P["fg_primary"],
            font=("Roboto", 11, "bold"),
            activebackground=P["accent"],
            activeforeground=P["fg_primary"],
            cursor="hand2",
            padx=10, pady=6,
        )

        # Frame MÚSICA (visible al inicio)
        self.cont_botones_music = tk.Frame(self.cont_botones_modo, bg=P["bg_card"])
        self.cont_botones_music.pack(side="top")

        self.boton_descargar_music_carat = tk.Button(
            self.cont_botones_music,
            text="Descargar Música con Carátula",
            command=lambda: self.disparar_proceso_descarga("music_caratula"),
            **_btn_kw,
        )
        self.boton_descargar_music_carat.pack(side="top", pady=5)

        self.boton_descargar_music_sin_carat = tk.Button(
            self.cont_botones_music,
            text="Descargar Música",
            command=lambda: self.disparar_proceso_descarga("music"),
            **_btn_kw,
        )
        self.boton_descargar_music_sin_carat.pack(side="top", pady=5)

        # Frame VIDEO (oculto al inicio)
        self.cont_botones_video = tk.Frame(self.cont_botones_modo, bg=P["bg_card"])

        self.boton_descargar_video_1080 = tk.Button(
            self.cont_botones_video,
            text="Descargar Video 1080p",
            command=lambda: self.disparar_proceso_descarga("video_1080"),
            **_btn_kw,
        )
        self.boton_descargar_video_1080.pack(side="top", pady=5)

        self.boton_descargar_video_720 = tk.Button(
            self.cont_botones_video,
            text="Descargar Video 720p",
            command=lambda: self.disparar_proceso_descarga("video_720"),
            **_btn_kw,
        )
        self.boton_descargar_video_720.pack(side="top", pady=5)

        # Barra de progreso
        self.barra_progreso = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(
            self.cont_mitad_izquierda,
            style="Purple.Horizontal.TProgressbar",
            variable=self.barra_progreso,
            maximum=100,
        )
        self.progressbar.pack(side="top", pady=12, fill="x", padx=24)
        self.barra_progreso.set(0)

    # ================================================================
    # COLA DE DESCARGAS
    # ================================================================
    def cola_de_descarga(self):
        """Panel derecho: lista visual de tareas en cola"""
        self.cola_de_descarga = tk.Frame(
            self.cont_mitad_derecha,
            bg=P["bg_queue"],
        )
        self.cola_de_descarga.pack(side="top", fill="both", expand=True)

        # Franja de acento superior de la cola
        tk.Frame(self.cola_de_descarga, bg=P["accent"], height=3).pack(
            side="top", fill="x")

        # Título del panel
        tk.Label(
            self.cola_de_descarga,
            text="Cola de descargas",
            bg=P["bg_queue"],
            fg=P["accent_light"],
            font=("Roboto", 12, "bold")
        ).pack(side="top", pady=(8, 4))

        # Separador
        tk.Frame(self.cola_de_descarga, bg=P["separator"], height=1).pack(
            side="top", fill="x", padx=10, pady=(0, 6))

        # Contenedor con scrollbar
        _frame_lista = tk.Frame(self.cola_de_descarga, bg=P["bg_queue"])
        _frame_lista.pack(side="top", fill="both", expand=True, padx=8, pady=(0, 8))

        _scrollbar = ttk.Scrollbar(
            _frame_lista,
            style="Purple.Vertical.TScrollbar",
            orient="vertical",
        )
        _scrollbar.pack(side="right", fill="y")

        self.lista_cola = tk.Listbox(
            _frame_lista,
            bg=P["list_bg"],
            fg=P["list_fg"],
            relief="flat",
            selectbackground=P["list_select"],
            selectforeground=P["fg_primary"],
            highlightthickness=0,
            font=("Roboto", 9),
            yscrollcommand=_scrollbar.set,
        )
        self.lista_cola.pack(side="left", fill="both", expand=True)
        _scrollbar.config(command=self.lista_cola.yview)

        # Estado interno de tareas
        self.tareas = {}
        self._contador_tareas = 0

    # ================================================================
    # GESTIÓN DE TAREAS
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
            self.boton_menu_music.config(bg=P["accent"],    fg=P["fg_primary"])
            self.boton_menu_video.config(bg=P["accent_dim"], fg=P["fg_secondary"])
            self.cont_botones_video.pack_forget()
            self.cont_botones_music.pack(side="top")

        elif modo == "video":
            self.boton_menu_video.config(bg=P["accent"],    fg=P["fg_primary"])
            self.boton_menu_music.config(bg=P["accent_dim"], fg=P["fg_secondary"])
            self.cont_botones_music.pack_forget()
            self.cont_botones_video.pack(side="top")

    # ================================================================
    # LÓGICA DE DESCARGA
    # ================================================================
    def disparar_proceso_descarga(self, tipo_media):
        """Maneja el clic en cualquier botón de descarga"""
        imagen_pil, url_obtenida = MotorDescarga.process_boton_descarga(self.entry_url)

        if imagen_pil is None:
            return

        self.foto_lista = ImageTk.PhotoImage(imagen_pil)
        self.etiqueta_caratula.config(image=self.foto_lista)
        self.etiqueta_caratula.image = self.foto_lista
        print(f"Éxito: Mostrando carátula de {url_obtenida}")

        self.barra_progreso.set(0)
        tid = self.agregar_tarea(url_obtenida)

        on_prog = lambda p: self.after(0, self.barra_progreso.set, p)
        on_fin  = lambda e, d: self.after(0, self._cerrar_tarea, tid, e, d)

        if tipo_media == "music":
            MotorDescarga.Descargar_Musica(on_prog, on_fin)
        elif tipo_media == "music_caratula":
            MotorDescarga.Descargar_Musica_Caratula(on_prog, on_fin)
        elif tipo_media == "video_1080":
            MotorDescarga.Descargar_Video_1080p(on_prog, on_fin)
        elif tipo_media == "video_720":
            MotorDescarga.Descargar_Video_720p(on_prog, on_fin)

    def cambiar_carpeta_descargas(self):
        """Abre el selector de carpeta y guarda la nueva ruta."""
        import os

        nueva_ruta = filedialog.askdirectory(
            title="Selecciona la carpeta de descargas",
            initialdir=MotorDescarga.ruta_base
        )

        if not nueva_ruta:
            return

        confirmar = messagebox.askyesno(
            "Cambiar carpeta",
            f"¿Cambiar la carpeta de descargas a:\n\n{nueva_ruta}?"
        )

        if confirmar:
            MotorDescarga.set_ruta_descargas(nueva_ruta)
            MotorDescarga.ruta_base = nueva_ruta

            for carpeta in MotorDescarga.carpetas:
                os.makedirs(os.path.join(nueva_ruta, carpeta), exist_ok=True)

            messagebox.showinfo(
                "Carpeta cambiada",
                f"Las descargas se guardarán en:\n\n{nueva_ruta}"
            )
            print(f"[UI] Ruta de descargas actualizada: {nueva_ruta}")