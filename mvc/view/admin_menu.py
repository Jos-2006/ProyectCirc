import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from controller.admin_controller import AdminController


class AdminMenu:
    """Vista del modulo administrador."""

    def __init__(self, root: tk.Tk, logout_callback) -> None:
        self.root = root
        self.logout_callback = logout_callback
        self.controller = AdminController()
        self._construir_gui()

    def _construir_gui(self) -> None:
        self.root.title("Sistema de Circo - Administrador")

        sidebar = tk.Frame(self.root, bg="#1E4A8C", width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="Administrador",
            bg="#1E4A8C",
            fg="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(18, 8))

        tk.Label(
            sidebar,
            text="Gestion integral\nde shows",
            bg="#1E4A8C",
            fg="#DDE6FF",
            font=("Segoe UI", 10),
            justify="center",
        ).pack(pady=(0, 18))

        tk.Button(
            sidebar,
            text="Cargar shows demo",
            command=self._cargar_demo,
            bg="#4E7AC7",
            fg="white",
            relief="flat",
        ).pack(fill="x", padx=14, pady=(0, 6))

        tk.Button(
            sidebar,
            text="Refrescar datos",
            command=self._cargar_eventos,
            bg="#4E7AC7",
            fg="white",
            relief="flat",
        ).pack(fill="x", padx=14, pady=(0, 6))

        tk.Button(
            sidebar,
            text="Cerrar sesion",
            command=self.logout_callback,
            bg="#B00020",
            fg="white",
            relief="flat",
        ).pack(fill="x", padx=14, pady=(20, 0))

        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        self._crear_tabla_eventos()
        self._crear_formulario_evento()
        self._crear_gestion_precios()
        self._crear_bloque_reportes()
        self._cargar_eventos()

    def _crear_tabla_eventos(self) -> None:
        tabla_frame = tk.LabelFrame(self.content, text="Cartelera de shows", bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=14, pady=(10, 6))

        columnas = ("id", "nombre", "categoria", "fecha", "hora", "duracion", "general")
        self.tree_eventos = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)
        encabezados = {
            "id": "ID",
            "nombre": "Show",
            "categoria": "Categoria",
            "fecha": "Fecha",
            "hora": "Hora",
            "duracion": "Duracion",
            "general": "Precio G",
        }
        for columna in columnas:
            self.tree_eventos.heading(columna, text=encabezados[columna])
            self.tree_eventos.column(columna, width=90, anchor="center")
        self.tree_eventos.column("nombre", width=160, anchor="w")
        self.tree_eventos.pack(fill="both", expand=True, padx=8, pady=8)

    def _crear_formulario_evento(self) -> None:
        form = tk.LabelFrame(self.content, text="Registrar show", bg="white")
        form.pack(fill="x", padx=14, pady=(0, 6))

        tk.Label(form, text="Nombre", bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.entry_nombre = tk.Entry(form)
        self.entry_nombre.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Categoria", bg="white").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.combo_categoria = ttk.Combobox(
            form,
            values=["Acrobacia", "Magia", "Comedia", "Fuego", "Musical"],
            state="readonly",
        )
        self.combo_categoria.set("Acrobacia")
        self.combo_categoria.grid(row=0, column=3, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Fecha (YYYY-MM-DD)", bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.entry_fecha = tk.Entry(form)
        self.entry_fecha.grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Hora (HH:MM)", bg="white").grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.entry_hora = tk.Entry(form)
        self.entry_hora.grid(row=1, column=3, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Duracion (min)", bg="white").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.entry_duracion = tk.Entry(form)
        self.entry_duracion.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Descripcion", bg="white").grid(row=2, column=2, sticky="w", padx=5, pady=3)
        self.entry_descripcion = tk.Entry(form)
        self.entry_descripcion.grid(row=2, column=3, sticky="ew", padx=5, pady=3)

        tk.Button(
            form,
            text="Programar show",
            command=self._programar_evento,
            bg="#1E4A8C",
            fg="white",
            relief="flat",
        ).grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Cargar show",
            command=self._cargar_evento_en_formulario,
            bg="#7A8AA8",
            fg="white",
            relief="flat",
        ).grid(row=4, column=0, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Actualizar show",
            command=self._actualizar_show,
            bg="#4E7AC7",
            fg="white",
            relief="flat",
        ).grid(row=4, column=1, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Ver detalle show",
            command=self._ver_detalle_evento,
            bg="#4E7AC7",
            fg="white",
            relief="flat",
        ).grid(row=3, column=2, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Eliminar show",
            command=self._eliminar_evento,
            bg="#7A8AA8",
            fg="white",
            relief="flat",
        ).grid(row=3, column=3, sticky="ew", padx=5, pady=6)

        for columna in range(4):
            form.grid_columnconfigure(columna, weight=1)

    def _crear_gestion_precios(self) -> None:
        frame = tk.LabelFrame(self.content, text="Gestion de precios por zona", bg="white")
        frame.pack(fill="x", padx=14, pady=(0, 6))

        tk.Label(frame, text="General", bg="white").grid(row=0, column=0, padx=5, pady=4)
        self.entry_precio_general = tk.Entry(frame, width=10)
        self.entry_precio_general.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame, text="Preferencial", bg="white").grid(row=0, column=2, padx=5, pady=4)
        self.entry_precio_preferencial = tk.Entry(frame, width=10)
        self.entry_precio_preferencial.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame, text="VIP", bg="white").grid(row=0, column=4, padx=5, pady=4)
        self.entry_precio_vip = tk.Entry(frame, width=10)
        self.entry_precio_vip.grid(row=0, column=5, padx=5, pady=4)

        tk.Button(
            frame,
            text="Actualizar precios show seleccionado",
            command=self._actualizar_precios,
            bg="#4E7AC7",
            fg="white",
            relief="flat",
        ).grid(row=0, column=6, padx=8, pady=4)

        tk.Label(frame, text="+ General", bg="white").grid(row=1, column=0, padx=5, pady=4)
        self.entry_mas_general = tk.Entry(frame, width=10)
        self.entry_mas_general.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame, text="+ Preferencial", bg="white").grid(row=1, column=2, padx=5, pady=4)
        self.entry_mas_preferencial = tk.Entry(frame, width=10)
        self.entry_mas_preferencial.grid(row=1, column=3, padx=5, pady=4)

        tk.Label(frame, text="+ VIP", bg="white").grid(row=1, column=4, padx=5, pady=4)
        self.entry_mas_vip = tk.Entry(frame, width=10)
        self.entry_mas_vip.grid(row=1, column=5, padx=5, pady=4)

        tk.Button(
            frame,
            text="Agregar asientos",
            command=self._agregar_asientos,
            bg="#1E4A8C",
            fg="white",
            relief="flat",
        ).grid(row=1, column=6, padx=8, pady=4)

    def _crear_bloque_reportes(self) -> None:
        frame = tk.LabelFrame(self.content, text="Reportes y consultas", bg="white")
        frame.pack(fill="x", padx=14, pady=(0, 10))

        tk.Button(
            frame,
            text="Reporte del show seleccionado",
            command=self._reporte_evento,
            bg="#1E4A8C",
            fg="white",
            relief="flat",
        ).grid(row=0, column=0, padx=5, pady=4)

        tk.Button(
            frame,
            text="Reporte general",
            command=self._reporte_general,
            bg="#1E4A8C",
            fg="white",
            relief="flat",
        ).grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame, text="Fecha", bg="white").grid(row=0, column=2, padx=(20, 5), pady=4)
        self.entry_fecha_reporte = tk.Entry(frame, width=12)
        self.entry_fecha_reporte.grid(row=0, column=3, padx=5, pady=4)

        tk.Button(
            frame,
            text="Reporte por fecha",
            command=self._reporte_por_fecha,
            bg="#4E7AC7",
            fg="white",
            relief="flat",
        ).grid(row=0, column=4, padx=5, pady=4)

        tk.Label(frame, text="Ticket ID", bg="white").grid(row=1, column=0, padx=5, pady=4)
        self.entry_ticket_id = tk.Entry(frame, width=10)
        self.entry_ticket_id.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        tk.Button(
            frame,
            text="Consultar ticket",
            command=self._consultar_ticket,
            bg="#7A8AA8",
            fg="white",
            relief="flat",
        ).grid(row=1, column=2, padx=5, pady=4)

    def _seleccion_evento_id(self) -> Optional[int]:
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
                    evento.duracion_minutos,
                    f"{evento.precios_por_zona.get('General', 0):.0f}",
                ),
            )

    def _programar_evento(self) -> None:
        try:
            duracion = int(self.entry_duracion.get().strip())
        except ValueError:
            messagebox.showerror("Dato invalido", "La duracion debe ser un numero entero.")
            return

        ok, mensaje, _ = self.controller.programar_evento(
            nombre=self.entry_nombre.get().strip(),
            categoria=self.combo_categoria.get().strip(),
            fecha=self.entry_fecha.get().strip(),
            hora_inicio=self.entry_hora.get().strip(),
            duracion_minutos=duracion,
            descripcion=self.entry_descripcion.get().strip(),
        )

        if not ok:
            messagebox.showerror("No se pudo programar", mensaje)
            return

        messagebox.showinfo("Exito", mensaje)
        self.entry_nombre.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self._cargar_eventos()

    def _cargar_evento_en_formulario(self) -> None:
        evento_id = self._seleccion_evento_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show.")
            return

        evento = self.controller.obtener_evento(evento_id)
        if evento is None:
            messagebox.showerror("Error", "No se encontro el show.")
            return

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, evento.nombre)
        self.combo_categoria.set(evento.categoria)
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, evento.fecha)
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, evento.hora_inicio)
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, str(evento.duracion_minutos))
        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, evento.descripcion)

        self.entry_precio_general.delete(0, tk.END)
        self.entry_precio_general.insert(0, str(int(evento.precios_por_zona.get("General", 0))))
        self.entry_precio_preferencial.delete(0, tk.END)
        self.entry_precio_preferencial.insert(0, str(int(evento.precios_por_zona.get("Preferencial", 0))))
        self.entry_precio_vip.delete(0, tk.END)
        self.entry_precio_vip.insert(0, str(int(evento.precios_por_zona.get("VIP", 0))))

    def _actualizar_show(self) -> None:
        evento_id = self._seleccion_evento_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show para actualizar.")
            return

        try:
            duracion = int(self.entry_duracion.get().strip())
        except ValueError:
            messagebox.showerror("Dato invalido", "La duracion debe ser un numero entero.")
            return

        ok, mensaje = self.controller.actualizar_evento(
            evento_id=evento_id,
            nombre=self.entry_nombre.get().strip(),
            categoria=self.combo_categoria.get().strip(),
            fecha=self.entry_fecha.get().strip(),
            hora_inicio=self.entry_hora.get().strip(),
            duracion_minutos=duracion,
            descripcion=self.entry_descripcion.get().strip(),
        )
        if ok:
            messagebox.showinfo("Exito", mensaje)
            self._cargar_eventos()
        else:
            messagebox.showerror("Error", mensaje)

    def _ver_detalle_evento(self) -> None:
        evento_id = self._seleccion_evento_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show.")
            return

        evento = self.controller.obtener_evento(evento_id)
        if evento is None:
            messagebox.showerror("Error", "No se encontro el show.")
            return

        detalle = (
            f"ID: {evento.identificador}\n"
            f"Show: {evento.nombre}\n"
            f"Categoria: {evento.categoria}\n"
            f"Fecha: {evento.fecha}\n"
            f"Hora: {evento.hora_inicio}\n"
            f"Duracion: {evento.duracion_minutos} min\n"
            f"Descripcion: {evento.descripcion}\n\n"
            f"Precios:\n"
            f"- General: {evento.precios_por_zona.get('General', 0):.2f}\n"
            f"- Preferencial: {evento.precios_por_zona.get('Preferencial', 0):.2f}\n"
            f"- VIP: {evento.precios_por_zona.get('VIP', 0):.2f}"
        )
        messagebox.showinfo("Detalle del show", detalle)

    def _eliminar_evento(self) -> None:
        evento_id = self._seleccion_evento_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show.")
            return

        ok, mensaje = self.controller.eliminar_evento(evento_id)
        if ok:
            messagebox.showinfo("Exito", mensaje)
            self._cargar_eventos()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    def _actualizar_precios(self) -> None:
        evento_id = self._seleccion_evento_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show para actualizar precios.")
            return

        try:
            general = float(self.entry_precio_general.get().strip())
            preferencial = float(self.entry_precio_preferencial.get().strip())
            vip = float(self.entry_precio_vip.get().strip())
        except ValueError:
            messagebox.showerror("Dato invalido", "Los precios deben ser numericos.")
            return

        ok, mensaje = self.controller.actualizar_precios(evento_id, general, preferencial, vip)
        if ok:
            messagebox.showinfo("Exito", mensaje)
            self._cargar_eventos()
        else:
            messagebox.showerror("Error", mensaje)

    def _agregar_asientos(self) -> None:
        evento_id = self._seleccion_evento_id()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show para agregar asientos.")
            return

        try:
            general = int((self.entry_mas_general.get() or "0").strip())
            preferencial = int((self.entry_mas_preferencial.get() or "0").strip())
            vip = int((self.entry_mas_vip.get() or "0").strip())
        except ValueError:
            messagebox.showerror("Dato invalido", "Los asientos deben ser numeros enteros.")
            return

        ok, mensaje = self.controller.aumentar_capacidad(
            evento_id=evento_id,
            agregar_general=general,
            agregar_preferencial=preferencial,
            agregar_vip=vip,
        )
        if ok:
            messagebox.showinfo("Exito", mensaje)
            self.entry_mas_general.delete(0, tk.END)
            self.entry_mas_preferencial.delete(0, tk.END)
            self.entry_mas_vip.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)

    def _reporte_evento(self) -> None:
        evento_id = self._seleccion_evento_id()
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
            "Ventas por zona:",
        ]
        for zona, datos in reporte["por_zona"].items():
            lineas.append(
                f"- {zona}: vendidos {datos['vendidos']} / {datos['capacidad']} | "
                f"disponibles {datos['disponibles']} | recaudado {datos['recaudado']:.2f}"
            )
        lineas.extend(
            [
                "",
                f"Total vendidos: {reporte['total_vendidos']}",
                f"Total recaudado: {reporte['total_recaudado']:.2f}",
                f"Ocupacion: {reporte['ocupacion']:.2f}%",
            ]
        )
        self._abrir_ventana_reporte("Reporte por show", "\n".join(lineas))

    def _reporte_general(self) -> None:
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
            "Ventas por categoria:",
        ]
        for categoria, ventas in reporte["ventas_por_categoria"].items():
            lineas.append(f"- {categoria}: {ventas} tickets")
        self._abrir_ventana_reporte("Reporte general", "\n".join(lineas))

    def _reporte_por_fecha(self) -> None:
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
            f"Show top ocupacion: {reporte['evento_top_nombre']}",
        ]
        self._abrir_ventana_reporte("Reporte por fecha", "\n".join(lineas))

    def _consultar_ticket(self) -> None:
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

    def _cargar_demo(self) -> None:
        agregados = self.controller.cargar_shows_demo()
        messagebox.showinfo("Shows demo", f"Se agregaron {agregados} shows de ejemplo.")
        self._cargar_eventos()

    def _abrir_ventana_reporte(self, titulo: str, contenido: str) -> None:
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("690x430")

        texto = tk.Text(ventana, wrap="word", font=("Consolas", 10))
        texto.pack(fill="both", expand=True, padx=10, pady=10)
        texto.insert("1.0", contenido)
        texto.config(state=tk.DISABLED)

