import tkinter as tk
from tkinter import messagebox, ttk

from controller.cliente_controller import ClienteController


class ClienteMenu:
    """Vista del modulo cliente."""

    def __init__(self, root: tk.Tk, usuario_id: int, logout_callback) -> None:
        self.root = root
        self.usuario_id = usuario_id
        self.logout_callback = logout_callback
        self.controller = ClienteController()
        self._construir_gui()

    def _construir_gui(self) -> None:
        self.root.title("Sistema de Circo - Cliente")

        sidebar = tk.Frame(self.root, bg="#1E4A8C", width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="Cliente",
            bg="#1E4A8C",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 8))

        tk.Button(
            sidebar,
            text="Ver cartelera",
            command=self._mostrar_cartelera,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).pack(fill="x", padx=14, pady=(0, 6))

        tk.Button(
            sidebar,
            text="Mis tickets",
            command=self._mostrar_tickets,
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

        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        self._construir_panel_cartelera()
        self._construir_panel_tickets()
        self._mostrar_cartelera()

    def _construir_panel_cartelera(self) -> None:
        self.panel_cartelera = tk.Frame(self.content, bg="white")

        columnas = ("id", "nombre", "categoria", "fecha", "hora", "general")
        self.tree_cartelera = ttk.Treeview(self.panel_cartelera, columns=columnas, show="headings", height=8)
        titulos = {
            "id": "ID",
            "nombre": "Show",
            "categoria": "Categoria",
            "fecha": "Fecha",
            "hora": "Hora",
            "general": "Precio G"
        }
        for col in columnas:
            self.tree_cartelera.heading(col, text=titulos[col])
            self.tree_cartelera.column(col, width=100, anchor="center")
        self.tree_cartelera.column("nombre", width=180, anchor="w")
        self.tree_cartelera.bind("<<TreeviewSelect>>", self._on_event_select)
        self.tree_cartelera.pack(fill="both", expand=True, padx=14, pady=(10, 6))

        compra_frame = tk.Frame(self.panel_cartelera, bg="white")
        compra_frame.pack(fill="x", padx=14, pady=(0, 10))
        tk.Label(
            compra_frame,
            text="Compra de entrada",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=6, pady=(0, 4))

        tk.Label(compra_frame, text="Zona", bg="white").grid(row=1, column=0, padx=6, pady=4)
        self.zona_var = tk.StringVar(value="General")
        for idx, zona in enumerate(("General", "Preferencial", "VIP"), start=1):
            tk.Radiobutton(
                compra_frame,
                text=zona,
                value=zona,
                variable=self.zona_var,
                bg="white"
            ).grid(row=1, column=idx, padx=3, pady=4)

        tk.Label(compra_frame, text="Metodo pago", bg="white").grid(row=2, column=0, padx=6, pady=4)
        self.combo_pago = ttk.Combobox(
            compra_frame,
            values=["Tarjeta", "Efectivo", "Transferencia"],
            state="readonly",
            width=20
        )
        self.combo_pago.set("Tarjeta")
        self.combo_pago.grid(row=2, column=1, columnspan=2, sticky="w", padx=3, pady=4)

        self.label_disponibles = tk.Label(compra_frame, text="Disponibles: -", bg="white")
        self.label_disponibles.grid(row=3, column=0, columnspan=4, sticky="w", padx=6)

        tk.Button(
            compra_frame,
            text="Ver detalle show",
            command=self._ver_detalle_show,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).grid(row=1, column=4, padx=6, pady=4)

        tk.Button(
            compra_frame,
            text="Comprar entrada",
            command=self._comprar,
            bg="#1E4A8C",
            fg="white",
            relief="flat"
        ).grid(row=2, column=4, padx=6, pady=4)

        tk.Button(
            compra_frame,
            text="Refrescar cartelera",
            command=self._cargar_eventos,
            bg="#7A8AA8",
            fg="white",
            relief="flat"
        ).grid(row=3, column=4, padx=6, pady=4)

    def _construir_panel_tickets(self) -> None:
        self.panel_tickets = tk.Frame(self.content, bg="white")

        columnas = ("id", "show", "fecha", "hora", "zona", "asiento", "precio", "metodo")
        self.tree_tickets = ttk.Treeview(self.panel_tickets, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree_tickets.heading(col, text=col.capitalize())
            self.tree_tickets.column(col, width=95, anchor="center")
        self.tree_tickets.column("show", width=170, anchor="w")
        self.tree_tickets.pack(fill="both", expand=True, padx=14, pady=10)

    def _mostrar_cartelera(self) -> None:
        self.panel_tickets.pack_forget()
        self.panel_cartelera.pack(fill="both", expand=True)
        self._cargar_eventos()

    def _mostrar_tickets(self) -> None:
        self.panel_cartelera.pack_forget()
        self.panel_tickets.pack(fill="both", expand=True)
        self._cargar_tickets()

    def _evento_seleccionado_id(self):
        seleccion = self.tree_cartelera.selection()
        if not seleccion:
            return None
        item = self.tree_cartelera.item(seleccion[0])
        return int(item["values"][0])

    def _cargar_eventos(self) -> None:
        for item in self.tree_cartelera.get_children():
            self.tree_cartelera.delete(item)

        for evento in self.controller.listar_eventos():
            self.tree_cartelera.insert(
                "",
                tk.END,
                values=(
                    evento.identificador,
                    evento.nombre,
                    evento.categoria,
                    evento.fecha,
                    evento.hora_inicio,
                    f"{evento.precios_por_zona.get('General', 0):.0f}"
                )
            )

    def _cargar_tickets(self) -> None:
        for item in self.tree_tickets.get_children():
            self.tree_tickets.delete(item)

        for ticket in self.controller.tickets_del_usuario(self.usuario_id):
            evento = self.controller.detalle_evento(ticket.evento_id)
            nombre_show = "-"
            fecha_show = "-"
            hora_show = "-"
            if evento is not None:
                nombre_show = evento.nombre
                fecha_show = evento.fecha
                hora_show = evento.hora_inicio

            self.tree_tickets.insert(
                "",
                tk.END,
                values=(
                    ticket.identificador,
                    nombre_show,
                    fecha_show,
                    hora_show,
                    ticket.zona,
                    ticket.numero_asiento,
                    f"{ticket.precio:.2f}",
                    ticket.metodo_pago
                )
            )

    def _on_event_select(self, _event) -> None:
        evento_id = self._evento_seleccionado_id()
        if evento_id is None:
            self.label_disponibles.config(text="Disponibles: -")
            return

        disponibles = self.controller.asientos_disponibles(evento_id)
        if disponibles is None:
            self.label_disponibles.config(text="Disponibles: -")
            return

        texto = "Disponibles: " + ", ".join(f"{zona} {cantidad}" for zona, cantidad in disponibles.items())
        self.label_disponibles.config(text=texto)

    def _ver_detalle_show(self) -> None:
        evento_id = self._evento_seleccionado_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show.")
            return

        evento = self.controller.detalle_evento(evento_id)
        if evento is None:
            messagebox.showerror("Error", "No se encontro el show.")
            return

        mensaje = (
            f"Show: {evento.nombre}\n"
            f"Categoria: {evento.categoria}\n"
            f"Fecha: {evento.fecha}\n"
            f"Hora: {evento.hora_inicio}\n"
            f"Duracion: {evento.duracion_minutos} min\n"
            f"Descripcion: {evento.descripcion}\n\n"
            f"Precios por zona:\n"
            f"General: {evento.precios_por_zona.get('General', 0):.2f}\n"
            f"Preferencial: {evento.precios_por_zona.get('Preferencial', 0):.2f}\n"
            f"VIP: {evento.precios_por_zona.get('VIP', 0):.2f}"
        )
        messagebox.showinfo("Detalle del show", mensaje)

    def _comprar(self) -> None:
        evento_id = self._evento_seleccionado_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show para comprar.")
            return

        zona = self.zona_var.get()
        metodo_pago = self.combo_pago.get().strip()

        ok, mensaje, ticket = self.controller.comprar_ticket(
            evento_id=evento_id,
            zona=zona,
            usuario_id=self.usuario_id,
            metodo_pago=metodo_pago
        )
        if not ok or ticket is None:
            messagebox.showerror("Compra no realizada", mensaje)
            return

        messagebox.showinfo(
            "Compra exitosa",
            f"Ticket #{ticket.identificador} | Zona {ticket.zona} | Asiento {ticket.numero_asiento}"
        )
        self._on_event_select(None)

