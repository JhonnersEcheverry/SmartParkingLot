import tkinter as tk
from tkinter import ttk, font

class ParkingLotGUI:
    """
    GUI Profesional para el Simulador de Parqueadero Inteligente.

    MEJORAS VISUALES:
    - Paleta de colores moderna y consistente
    - Tipografía profesional con fuentes personalizadas
    - Efectos visuales (sombras, degradados simulados, bordes redondeados)
    - Diseño de tarjetas (cards) para estadísticas
    - Visualización mejorada de espacios de parqueo
    - Botones con estilo moderno
    """

    # === PALETA DE COLORES ===
    # Definir colores como constantes para fácil modificación
    COLOR_PRIMARY = "#2C3E50"        # Azul oscuro (header)
    COLOR_SECONDARY = "#34495E"      # Azul gris (elementos secundarios)
    COLOR_ACCENT = "#3498DB"         # Azul brillante (acentos)
    COLOR_SUCCESS = "#27AE60"        # Verde (éxito/ocupado)
    COLOR_WARNING = "#F39C12"        # Naranja (advertencia/espera)
    COLOR_DANGER = "#E74C3C"         # Rojo (error/detener)
    COLOR_INFO = "#3498DB"           # Azul info
    COLOR_BG = "#ECF0F1"             # Fondo claro
    COLOR_CARD = "#FFFFFF"           # Blanco para tarjetas
    COLOR_TEXT_DARK = "#2C3E50"      # Texto oscuro
    COLOR_TEXT_LIGHT = "#FFFFFF"     # Texto claro
    COLOR_BORDER = "#BDC3C7"         # Bordes sutiles

    def __init__(self, root, start_callback, add_vehicle_callback, stop_callback, reset_callback):
        self.root = root
        self.root.title("🚗 Simulador de Parqueadero Inteligente - OS Concepts Demo")
        self.root.geometry("1000x800")  # Aumentado para mostrar todos los botones
        self.root.configure(bg=self.COLOR_BG)

        # Configurar fuentes personalizadas
        self.font_title = font.Font(family="Segoe UI", size=16, weight="bold")
        self.font_header = font.Font(family="Segoe UI", size=12, weight="bold")
        self.font_body = font.Font(family="Segoe UI", size=10)
        self.font_small = font.Font(family="Segoe UI", size=9)
        self.font_stats = font.Font(family="Segoe UI", size=14, weight="bold")

        # === HEADER  ===
        self._create_header()

        # === PANEL DE ESTADISTICAS ===
        self._create_statistics_panel()

        # === VISUALIZACION PARKING LOT ===
        self._create_parking_canvas()

        # === LOG DE EVENTOS ===
        self._create_event_log()

        # === BOTONES ===
        self._create_control_buttons(start_callback, add_vehicle_callback,
                                     stop_callback, reset_callback)

        # === BARRA DE ESTADO ===
        self._create_status_bar()

    def _create_header(self):
        """
        Crea el header con título y descripción.
        ESTILO: Fondo oscuro con texto claro (profesional).
        """
        header_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)  # Mantener altura fija

        # Título principal
        title = tk.Label(
            header_frame,
            text="Simulador de Parqueadero Inteligente",
            font=self.font_title,
            bg=self.COLOR_PRIMARY,
            fg=self.COLOR_TEXT_LIGHT
        )
        title.pack(pady=(15, 5))

        # Subtítulo
        subtitle = tk.Label(
            header_frame,
            text="Demostración de Conceptos de Sistemas Operativos: Semáforos, Locks y Threads",
            font=self.font_small,
            bg=self.COLOR_PRIMARY,
            fg="#95A5A6"  # Gris claro
        )
        subtitle.pack()

    def _create_statistics_panel(self):
        """
        Panel de estadísticas con diseño de tarjetas (cards).
        ESTILO: Cards individuales con sombras simuladas.
        """
        # Contenedor principal
        stats_container = tk.Frame(self.root, bg=self.COLOR_BG)
        stats_container.pack(pady=20, padx=20, fill=tk.X)

        # Título de sección
        section_title = tk.Label(
            stats_container,
            text="Estadísticas en Tiempo Real",
            font=self.font_header,
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT_DARK
        )
        section_title.pack(anchor="w", pady=(0, 10))

        # Frame para las 3 tarjetas de estadísticas
        cards_frame = tk.Frame(stats_container, bg=self.COLOR_BG)
        cards_frame.pack(fill=tk.X)

        # Card 1: Total Vehículos
        # Capturar el valor de retorno (el label)
        self.total_vehicles_label = self._create_stat_card(
            cards_frame,
            "Total Vehículos",
            "0",
            self.COLOR_INFO,
            0
        )

        # Card 2: Completados (vehículos que salieron)
        self.successful_parks_label = self._create_stat_card(
            cards_frame,
            "Completados",
            "0",
            self.COLOR_SUCCESS,
            1
        )

        # Card 3: Esperando
        self.waiting_now_label = self._create_stat_card(
            cards_frame,
            "Esperando",
            "0",
            self.COLOR_WARNING,
            2
        )

    def _create_stat_card(self, parent, title, value, color, column):
        """
        Crea una tarjeta individual de estadística.

        DISEÑO:
        - Fondo blanco con borde de color
        - Número grande y prominente
        - Título descriptivo
        - Efecto de sombra simulado con bordes
        """
        # Frame de la card con borde coloreado
        card = tk.Frame(
            parent,
            bg=self.COLOR_CARD,
            relief=tk.FLAT,
            borderwidth=0,
            highlightbackground=color,
            highlightthickness=3
        )
        card.grid(row=0, column=column, padx=10, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)

        # Padding interno
        inner_frame = tk.Frame(card, bg=self.COLOR_CARD)
        inner_frame.pack(padx=15, pady=15)

        # Título de la card
        title_label = tk.Label(
            inner_frame,
            text=title,
            font=self.font_body,
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_DARK
        )
        title_label.pack()

        # Valor grande (el número)
        value_label = tk.Label(
            inner_frame,
            text=value,
            font=self.font_stats,
            bg=self.COLOR_CARD,
            fg=color
        )
        value_label.pack(pady=(5, 0))

        return value_label  # Retornar para poder actualizarlo después

    def _create_parking_canvas(self):
        """
        Crea el canvas para visualizar los espacios de parqueo.
        """
        # Contenedor
        canvas_container = tk.Frame(self.root, bg=self.COLOR_BG, height=200)
        canvas_container.pack(pady=10, padx=20, fill=tk.X)
        canvas_container.pack_propagate(False)  # Mantener altura fija

        # Título de sección
        section_title = tk.Label(
            canvas_container,
            text="Estado del Parqueadero",
            font=self.font_header,
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT_DARK
        )
        section_title.pack(anchor="w", pady=(0, 10))

        # Canvas con borde
        canvas_frame = tk.Frame(canvas_container, bg=self.COLOR_CARD, relief=tk.FLAT)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#34495E",  # Fondo tipo asfalto oscuro
            highlightthickness=0,
            height=180,  # Altura fija para el canvas
            width=950    # Ancho fijo para el canvas (1000 - 2*20 padding - 10)
        )
        self.canvas.pack(padx=5, pady=5)
        self.spaces = []

    def _create_event_log(self):
        """
        Crea el área de log de eventos con scroll.
        """
        # Contenedor
        log_container = tk.Frame(self.root, bg=self.COLOR_BG, height=150)
        log_container.pack(pady=10, padx=20, fill=tk.X)
        log_container.pack_propagate(False)  # Mantener altura fija

        # Título
        section_title = tk.Label(
            log_container,
            text="Registro de Eventos",
            font=self.font_header,
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT_DARK
        )
        section_title.pack(anchor="w", pady=(0, 10))

        # Frame para listbox + scrollbar
        log_frame = tk.Frame(log_container, bg=self.COLOR_CARD)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        # Scrollbar
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox estilo consola
        self.log_box = tk.Listbox(
            log_frame,
            font=("Consolas", 9),  # Fuente monoespaciada
            bg="#2C3E50",           # Fondo oscuro
            fg="#ECF0F1",           # Texto claro
            selectbackground="#34495E",
            selectforeground="#FFFFFF",
            yscrollcommand=scrollbar.set,
            height=6,  # Reducido de 8 a 6 líneas
            borderwidth=0,
            highlightthickness=0
        )
        self.log_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_box.yview)

    def _create_control_buttons(self, start_cb, add_cb, stop_cb, reset_cb):
        """
        Crea los botones de control con estilo moderno.
        """
        # Contenedor
        button_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        button_frame.pack(pady=15, padx=20)

        # Configurar estilo para botones
        style = ttk.Style()
        style.theme_use('default')

        # Estilo para botón de inicio (verde)
        style.configure(
            "Start.TButton",
            font=self.font_body,
            padding=10
        )

        # Botón 1: Iniciar (verde)
        btn_start = tk.Button(
            button_frame,
            text="Iniciar Simulación",
            command=start_cb,
            font=self.font_body,
            bg=self.COLOR_SUCCESS,
            fg=self.COLOR_TEXT_LIGHT,
            activebackground="#229954",
            activeforeground=self.COLOR_TEXT_LIGHT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0
        )
        btn_start.grid(row=0, column=0, padx=8)

        # Botón 2: Agregar (azul)
        btn_add = tk.Button(
            button_frame,
            text="Agregar Vehículo",
            command=add_cb,
            font=self.font_body,
            bg=self.COLOR_ACCENT,
            fg=self.COLOR_TEXT_LIGHT,
            activebackground="#2E86C1",
            activeforeground=self.COLOR_TEXT_LIGHT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0
        )
        btn_add.grid(row=0, column=1, padx=8)

        # Botón 3: Detener (naranja)
        btn_stop = tk.Button(
            button_frame,
            text="⏸Detener",
            command=stop_cb,
            font=self.font_body,
            bg=self.COLOR_WARNING,
            fg=self.COLOR_TEXT_LIGHT,
            activebackground="#DC7633",
            activeforeground=self.COLOR_TEXT_LIGHT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0
        )
        btn_stop.grid(row=0, column=2, padx=8)

        # Botón 4: Reiniciar (rojo)
        btn_reset = tk.Button(
            button_frame,
            text="Reiniciar",
            command=reset_cb,
            font=self.font_body,
            bg=self.COLOR_DANGER,
            fg=self.COLOR_TEXT_LIGHT,
            activebackground="#C0392B",
            activeforeground=self.COLOR_TEXT_LIGHT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0
        )
        btn_reset.grid(row=0, column=3, padx=8)

        # Efectos hover (opcional, avanzado)
        self._add_button_hover_effect(btn_start, self.COLOR_SUCCESS, "#229954")
        self._add_button_hover_effect(btn_add, self.COLOR_ACCENT, "#2E86C1")
        self._add_button_hover_effect(btn_stop, self.COLOR_WARNING, "#DC7633")
        self._add_button_hover_effect(btn_reset, self.COLOR_DANGER, "#C0392B")

    def _add_button_hover_effect(self, button, normal_color, hover_color):
        """
        Agrega efecto hover a los botones (cambio de color al pasar el mouse).
        """
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    def _create_status_bar(self):
        """
        Barra de estado en la parte inferior.
        """
        status_bar = tk.Frame(self.root, bg=self.COLOR_SECONDARY, height=25)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            status_bar,
            text="⚡ Sistema listo  |  Python Threading  |  OS Concepts Demo",
            font=self.font_small,
            bg=self.COLOR_SECONDARY,
            fg=self.COLOR_TEXT_LIGHT,
            anchor="w",
            padx=10
        )
        self.status_label.pack(fill=tk.X)

    def init_spaces(self, capacidad):
        """
        Dibuja los espacios de parqueo con estilo mejorado.
        """
        self.canvas.delete("all")
        self.spaces.clear()

        # Calcular posiciones centradas
        # Canvas tiene ancho fijo de 950px
        canvas_width = 950
        total_width = capacidad * 140
        start_x = (canvas_width - total_width) // 2
        start_y = 20  # Más arriba para aprovechar el espacio

        for i in range(capacidad):
            x0 = start_x + i * 140 + 20
            y0 = start_y

            shadow = self.canvas.create_rectangle(
                x0 + 4, y0 + 4, x0 + 114, y0 + 124,
                fill="#2C3E50", outline=""
            )

            # Rectángulo principal del espacio
            rect = self.canvas.create_rectangle(
                x0, y0, x0 + 110, y0 + 120,
                fill=self.COLOR_SUCCESS,  # Verde para LIBRE
                outline="#1E8449",
                width=3
            )

            # Líneas de parqueo (decorativas)
            self.canvas.create_line(
                x0 + 10, y0, x0 + 10, y0 + 120,
                fill="#7F8C8D", width=2, dash=(5, 5)
            )
            self.canvas.create_line(
                x0 + 100, y0, x0 + 100, y0 + 120,
                fill="#7F8C8D", width=2, dash=(5, 5)
            )

            # Número del espacio
            text = self.canvas.create_text(
                x0 + 55, y0 + 60,
                text=f"#{i+1}",
                font=("Segoe UI", 20, "bold"),
                fill=self.COLOR_TEXT_LIGHT  # Blanco para mejor contraste
            )

            # Etiqueta "LIBRE"
            status_text = self.canvas.create_text(
                x0 + 55, y0 + 90,
                text="LIBRE",
                font=("Segoe UI", 10, "bold"),
                fill=self.COLOR_TEXT_LIGHT  # Blanco sobre verde
            )

            self.spaces.append((rect, text, status_text))

    def update_spaces(self, ocupados, capacidad):
        """
        Actualiza visualmente los espacios ocupados con animación de color.
        """
        for i, space_tuple in enumerate(self.spaces):
            rect = space_tuple[0]
            number_text = space_tuple[1]
            status_text = space_tuple[2] if len(space_tuple) > 2 else None

            if i < ocupados:
                # Espacio OCUPADO - rojo (como semáforo en rojo = detenerse)
                self.canvas.itemconfig(rect, fill=self.COLOR_DANGER, outline="#C0392B", width=3)
                if status_text:
                    self.canvas.itemconfig(status_text, text="OCUPADO", fill=self.COLOR_TEXT_LIGHT)
                if number_text:
                    self.canvas.itemconfig(number_text, fill=self.COLOR_TEXT_LIGHT)
            else:
                # Espacio LIBRE - verde (como semáforo en verde = puede pasar)
                self.canvas.itemconfig(rect, fill=self.COLOR_SUCCESS, outline="#1E8449", width=3)
                if status_text:
                    self.canvas.itemconfig(status_text, text="LIBRE", fill=self.COLOR_TEXT_LIGHT)
                if number_text:
                    self.canvas.itemconfig(number_text, fill=self.COLOR_TEXT_LIGHT)

    def log_event(self, message):
        """
        Muestra mensajes de eventos en el log.
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        self.log_box.insert(tk.END, formatted_message)
        self.log_box.yview(tk.END)  # Auto-scroll al final

        # Opcional: Limitar a 100 mensajes para no saturar
        if self.log_box.size() > 100:
            self.log_box.delete(0, 0)  # Eliminar el más antiguo

    def update_statistics(self, total_vehicles, successful_parks, waiting_now):
        """
        Actualiza las estadísticas en las tarjetas.
        """
        self.total_vehicles_label.config(text=str(total_vehicles))
        self.successful_parks_label.config(text=str(successful_parks))
        self.waiting_now_label.config(text=str(waiting_now))

        # Actualizar status bar
        status_msg = f"⚡ Activo  |  Vehículos: {total_vehicles}  |  Esperando: {waiting_now}  |  Estacionados: {successful_parks}"
        self.status_label.config(text=status_msg)
