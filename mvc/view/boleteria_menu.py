import tkinter as tk
from tkinter import messagebox, ttk

from controller.boleteria_controller import BoleteriaController


class BoleteriaMenu:
    """Vista del modulo de boleteria (cajero)."""

    def __init__(self, root: tk.Tk, logout_callback) -> None:
        self.root = root
        self.logout_callback = logout_callback
        self.controller = BoleteriaController()
        self._construir_gui()

    def _construir_gui(self) -> None:
        self.root.title("Sistema de Circo - Boleteria")

        sidebar = tk.Frame(self.root, bg="#1E4A8C", width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="Cajero",
            bg="#1E4A8C",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 8))

        tk.Button(
            sidebar,
            text="Refrescar cartelera",
            command=self._cargar_eventos,
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

        columnas = ("id", "nombre", "categoria", "fecha", "hora", "general")
        self.tree_eventos = ttk.Treeview(self.content, columns=columnas, show="headings", height=9)
        titulos = {
            "id": "ID",
            "nombre": "Show",
            "categoria": "Categoria",
            "fecha": "Fecha",
            "hora": "Hora",
            "general": "Precio G"
        }
        for col in columnas:
            self.tree_eventos.heading(col, text=titulos[col])
            self.tree_eventos.column(col, width=100, anchor="center")
        self.tree_eventos.column("nombre", width=180, anchor="w")
        self.tree_eventos.bind("<<TreeviewSelect>>", self._on_event_select)
        self.tree_eventos.pack(fill="both", expand=True, padx=14, pady=(10, 6))

        venta = tk.LabelFrame(self.content, text="Venta en taquilla", bg="white")
        venta.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(venta, text="Zona", bg="white").grid(row=0, column=0, padx=6, pady=4)
        self.zona_var = tk.StringVar(value="General")
        for idx, zona in enumerate(("General", "Preferencial", "VIP"), start=1):
            tk.Radiobutton(
                venta,
                text=zona,
                value=zona,
                variable=self.zona_var,
                bg="white"
            ).grid(row=0, column=idx, padx=3, pady=4)

        tk.Label(venta, text="Metodo pago", bg="white").grid(row=1, column=0, padx=6, pady=4)
        self.combo_pago = ttk.Combobox(
            venta,
            values=["Efectivo", "Tarjeta", "Transferencia"],
            state="readonly",
            width=20
        )
        self.combo_pago.set("Efectivo")
        self.combo_pago.grid(row=1, column=1, columnspan=2, sticky="w", padx=3, pady=4)

        self.label_disponibles = tk.Label(venta, text="Disponibles: -", bg="white")
        self.label_disponibles.grid(row=2, column=0, columnspan=4, sticky="w", padx=6, pady=4)

        tk.Button(
            venta,
            text="Ver detalle show",
            command=self._ver_detalle_show,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).grid(row=0, column=4, padx=6, pady=4)

        tk.Button(
            venta,
            text="Vender entrada",
            command=self._vender,
            bg="#1E4A8C",
            fg="white",
            relief="flat"
        ).grid(row=1, column=4, padx=6, pady=4)

        self._cargar_eventos()

    def _evento_seleccionado_id(self):
        seleccion = self.tree_eventos.selection()
        if not seleccion:
            return None
        item = self.tree_eventos.item(seleccion[0])
        return int(item["values"][0])

    def _cargar_eventos(self) -> None:
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
                    f"{evento.precios_por_zona.get('General', 0):.0f}"
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

        detalle = (
            f"Show: {evento.nombre}\n"
            f"Categoria: {evento.categoria}\n"
            f"Fecha: {evento.fecha}\n"
            f"Hora: {evento.hora_inicio}\n"
            f"Duracion: {evento.duracion_minutos} min\n"
            f"Descripcion: {evento.descripcion}"
        )
        messagebox.showinfo("Detalle del show", detalle)

    def _vender(self) -> None:
        evento_id = self._evento_seleccionado_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show para vender.")
            return

        ok, mensaje, ticket = self.controller.vender_ticket(
            evento_id=evento_id,
            zona=self.zona_var.get(),
            metodo_pago=self.combo_pago.get().strip()
        )
        if not ok or ticket is None:
            messagebox.showerror("Venta no realizada", mensaje)
            return

        messagebox.showinfo(
            "Venta exitosa",
            f"Ticket #{ticket.identificador} | Zona {ticket.zona} | Asiento {ticket.numero_asiento}"
        )
        self._on_event_select(None)

