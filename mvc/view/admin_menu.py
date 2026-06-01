import tkinter as tk
from tkinter import ttk
from typing import Optional

from controller.admin_controller import AdminController
from view.admin_price_panel import AdminPricePanel
from view.admin_report_panel import AdminReportPanel
from view.admin_show_dialog import AdminShowDialog


class AdminMenu:
    """Vista principal del modulo administrador."""

    def __init__(self, root: tk.Tk, logout_callback) -> None:
        self.root = root
        self.logout_callback = logout_callback
        self.controller = AdminController()
        self.construir_gui()

    def construir_gui(self) -> None:
        self.root.title("Sistema de Circo - Administrador")

        self.crear_sidebar()

        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        self.crear_tabla_eventos()

        self.panel_precios = AdminPricePanel(
            parent=self.content,
            controller=self.controller,
            seleccionar_evento_id_callback=self.seleccion_evento_id,
            refrescar_eventos_callback=self.cargar_eventos
        )
        self.panel_reportes = AdminReportPanel(
            parent=self.content,
            controller=self.controller,
            seleccionar_evento_id_callback=self.seleccion_evento_id
        )
        self.dialogo_shows = AdminShowDialog(
            root=self.root,
            controller=self.controller,
            seleccionar_evento_id_callback=self.seleccion_evento_id,
            refrescar_eventos_callback=self.cargar_eventos,
            cargar_precios_callback=self.cargar_precios_evento
        )

        self.cargar_eventos()

    def crear_sidebar(self) -> None:
        sidebar = tk.Frame(self.root, bg="#1E4A8C", width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="Administrador",
            bg="#1E4A8C",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(18, 8))

        tk.Label(
            sidebar,
            text="Gestion integral\nde shows",
            bg="#1E4A8C",
            fg="#DDE6FF",
            font=("Segoe UI", 10),
            justify="center"
        ).pack(pady=(0, 18))

        tk.Button(
            sidebar,
            text="ConfigShows",
            command=self.abrir_config_shows,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).pack(fill="x", padx=14, pady=(0, 6))

        tk.Button(
            sidebar,
            text="Refrescar datos",
            command=self.cargar_eventos,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).pack(fill="x", padx=14, pady=(0, 6))

        tk.Button(
            sidebar,
            text="Cerrar sesion",
            command=self.logout_callback,
            bg="#B00020",
            fg="white",
            relief="flat"
        ).pack(fill="x", padx=14, pady=(20, 0))

    def crear_tabla_eventos(self) -> None:
        tabla_frame = tk.Frame(self.content, bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=14, pady=(10, 6))

        tk.Label(
            tabla_frame,
            text="Cartelera de shows",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill="x", padx=2, pady=(0, 4))

        columnas = ("id", "nombre", "categoria", "fecha", "hora", "duracion", "general")
        self.tree_eventos = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)

        encabezados = {
            "id": "ID",
            "nombre": "Show",
            "categoria": "Categoria",
            "fecha": "Fecha",
            "hora": "Hora",
            "duracion": "Duracion",
            "general": "Precio G"
        }

        for columna in columnas:
            self.tree_eventos.heading(columna, text=encabezados[columna])
            self.tree_eventos.column(columna, width=90, anchor="center")
        self.tree_eventos.column("nombre", width=160, anchor="w")
        self.tree_eventos.pack(fill="both", expand=True)

    def seleccion_evento_id(self) -> Optional[int]:
        seleccion = self.tree_eventos.selection()
        if not seleccion:
            return None
        item = self.tree_eventos.item(seleccion[0])
        return int(item["values"][0])

    def cargar_eventos(self) -> None:
        for item in self.tree_eventos.get_children():
            self.tree_eventos.delete(item)

        for evento in self.controller.listar_eventos():
            self.tree_eventos.insert(
                "",
                tk.END,
                values=(
                    evento.identificador,
                    evento.nombre,
                    evento.categoria,
                    evento.fecha,
                    evento.hora_inicio,
                    evento.duracion_minutos,
                    f"{evento.precios_por_zona.get('General', 0):.0f}"
                )
            )

    def cargar_precios_evento(self, evento) -> None:
        self.panel_precios.cargar_precios_evento(evento)

    def abrir_config_shows(self) -> None:
        self.dialogo_shows.abrir()
