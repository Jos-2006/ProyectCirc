import tkinter as tk
from tkinter import messagebox


class AdminReportPanel:
    """Panel de reportes y consulta de ticket."""

    def __init__(self, parent, controller, seleccionar_evento_id_callback) -> None:
        self.controller = controller
        self.seleccionar_evento_id_callback = seleccionar_evento_id_callback
        self.crear_panel(parent)

    def crear_panel(self, parent) -> None:
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(
            frame,
            text="Reportes y consultas",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=5, pady=(0, 4))

        tk.Button(
            frame,
            text="Reporte del show seleccionado",
            command=self.reporte_evento,
            bg="#1E4A8C",
            fg="white",
            relief="flat"
        ).grid(row=1, column=0, padx=5, pady=4)

        tk.Button(
            frame,
            text="Reporte general",
            command=self.reporte_general,
            bg="#1E4A8C",
            fg="white",
            relief="flat"
        ).grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame, text="Fecha", bg="white").grid(row=1, column=2, padx=(20, 5), pady=4)
        self.entry_fecha_reporte = tk.Entry(frame, width=12)
        self.entry_fecha_reporte.grid(row=1, column=3, padx=5, pady=4)

        tk.Button(
            frame,
            text="Reporte por fecha",
            command=self.reporte_por_fecha,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).grid(row=1, column=4, padx=5, pady=4)

        tk.Label(frame, text="Ticket ID", bg="white").grid(row=2, column=0, padx=5, pady=4)
        self.entry_ticket_id = tk.Entry(frame, width=10)
        self.entry_ticket_id.grid(row=2, column=1, padx=5, pady=4, sticky="w")

        tk.Button(
            frame,
            text="Consultar ticket",
            command=self.consultar_ticket,
            bg="#7A8AA8",
            fg="white",
            relief="flat"
        ).grid(row=2, column=2, padx=5, pady=4)

    def reporte_evento(self) -> None:
        evento_id = self.seleccionar_evento_id_callback()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show para ver su reporte.")
            return

        reporte = self.controller.generar_reporte_evento(evento_id)
        if reporte is None:
            messagebox.showerror("Error", "No fue posible generar el reporte.")
            return

        lineas = [
            f"Show: {reporte['evento']} ({reporte['categoria']})",
            f"Fecha: {reporte['fecha']}  Hora: {reporte['hora_inicio']}",
            "",
            "Ventas por zona:"
        ]

        for zona, datos in reporte["por_zona"].items():
            lineas.append(
                f"- {zona}: vendidos {datos['vendidos']} / {datos['capacidad']} | "
                f"disponibles {datos['disponibles']} | recaudado {datos['recaudado']:.2f}"
            )

        lineas.append("")
        lineas.append(f"Total vendidos: {reporte['total_vendidos']}")
        lineas.append(f"Total recaudado: {reporte['total_recaudado']:.2f}")
        lineas.append(f"Ocupacion: {reporte['ocupacion']:.2f}%")
        self.abrir_ventana_reporte("Reporte por show", "\n".join(lineas))

    def reporte_general(self) -> None:
        reporte = self.controller.generar_reporte_general()
        lineas = [
            "Resumen general del circo",
            "",
            f"Total de shows: {reporte['total_eventos']}",
            f"Total de tickets vendidos: {reporte['total_tickets']}",
            f"Recaudacion total: {reporte['total_recaudado']:.2f}",
            f"Ocupacion promedio: {reporte['ocupacion_promedio']:.2f}%",
            f"Show con mayor ocupacion: {reporte['evento_top_nombre']}",
            "",
            "Ventas por categoria:"
        ]

        for categoria, ventas in reporte["ventas_por_categoria"].items():
            lineas.append(f"- {categoria}: {ventas} tickets")

        self.abrir_ventana_reporte("Reporte general", "\n".join(lineas))

    def reporte_por_fecha(self) -> None:
        fecha = self.entry_fecha_reporte.get().strip()
        if not fecha:
            messagebox.showwarning("Dato requerido", "Ingresa la fecha a consultar.")
            return

        reporte = self.controller.generar_reporte_por_fecha(fecha)
        lineas = [
            f"Reporte filtrado por fecha: {reporte['fecha_consultada']}",
            "",
            f"Shows en fecha: {reporte['total_eventos']}",
            f"Tickets vendidos: {reporte['total_tickets']}",
            f"Recaudacion: {reporte['total_recaudado']:.2f}",
            f"Show top ocupacion: {reporte['evento_top_nombre']}"
        ]
        self.abrir_ventana_reporte("Reporte por fecha", "\n".join(lineas))

    def consultar_ticket(self) -> None:
        try:
            ticket_id = int(self.entry_ticket_id.get().strip())
        except ValueError:
            messagebox.showerror("Dato invalido", "Ticket ID debe ser numero entero.")
            return

        ticket = self.controller.buscar_ticket(ticket_id)
        if ticket is None:
            messagebox.showwarning("No encontrado", "No existe ese ticket.")
            return

        detalle = (
            f"Ticket #{ticket.identificador}\n"
            f"Evento ID: {ticket.evento_id}\n"
            f"Zona: {ticket.zona}\n"
            f"Asiento: {ticket.numero_asiento}\n"
            f"Precio: {ticket.precio:.2f}\n"
            f"Fecha compra: {ticket.fecha_compra}\n"
            f"Metodo pago: {ticket.metodo_pago}"
        )
        messagebox.showinfo("Consulta individual de ticket", detalle)

    def abrir_ventana_reporte(self, titulo: str, contenido: str) -> None:
        ventana = tk.Toplevel()
        ventana.title(titulo)
        ventana.geometry("690x430")

        texto = tk.Text(ventana, wrap="word", font=("Consolas", 10))
        texto.pack(fill="both", expand=True, padx=10, pady=10)
        texto.insert("1.0", contenido)
        texto.config(state=tk.DISABLED)
