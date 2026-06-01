import tkinter as tk
from tkinter import messagebox, ttk


class AdminShowDialog:
    """Ventana secundaria para crear y editar shows."""

    def __init__(
        self,
        root,
        controller,
        seleccionar_evento_id_callback,
        refrescar_eventos_callback,
        cargar_precios_callback
    ) -> None:
        self.root = root
        self.controller = controller
        self.seleccionar_evento_id_callback = seleccionar_evento_id_callback
        self.refrescar_eventos_callback = refrescar_eventos_callback
        self.cargar_precios_callback = cargar_precios_callback
        self.ventana = None

    def abrir(self) -> None:
        if self.ventana is not None and self.ventana.winfo_exists():
            self.ventana.lift()
            self.ventana.focus_force()
            return

        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Gestion de shows")
        self.ventana.geometry("980x300")
        self.ventana.configure(bg="white")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.crear_formulario(self.ventana)

    def cerrar(self) -> None:
        if self.ventana is not None and self.ventana.winfo_exists():
            self.ventana.destroy()
        self.ventana = None

    def crear_formulario(self, parent) -> None:
        form = tk.Frame(parent, bg="white")
        form.pack(fill="both", expand=True, padx=14, pady=10)

        tk.Label(
            form,
            text="Gestion de shows",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=5, pady=(0, 5))

        tk.Label(
            form,
            text="Selecciona un show en la tabla principal para cargar, actualizar o eliminar.",
            bg="white",
            fg="#505050"
        ).grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=(0, 8))

        tk.Label(form, text="Nombre", bg="white").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.entry_nombre = tk.Entry(form)
        self.entry_nombre.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Categoria", bg="white").grid(row=2, column=2, sticky="w", padx=5, pady=3)
        self.combo_categoria = ttk.Combobox(
            form,
            values=["Acrobacia", "Magia", "Comedia", "Fuego", "Musical"],
            state="readonly"
        )
        self.combo_categoria.set("Acrobacia")
        self.combo_categoria.grid(row=2, column=3, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Fecha (YYYY-MM-DD)", bg="white").grid(row=3, column=0, sticky="w", padx=5, pady=3)
        self.entry_fecha = tk.Entry(form)
        self.entry_fecha.grid(row=3, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Hora (HH:MM)", bg="white").grid(row=3, column=2, sticky="w", padx=5, pady=3)
        self.entry_hora = tk.Entry(form)
        self.entry_hora.grid(row=3, column=3, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Duracion (min)", bg="white").grid(row=4, column=0, sticky="w", padx=5, pady=3)
        self.entry_duracion = tk.Entry(form)
        self.entry_duracion.grid(row=4, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form, text="Descripcion", bg="white").grid(row=4, column=2, sticky="w", padx=5, pady=3)
        self.entry_descripcion = tk.Entry(form)
        self.entry_descripcion.grid(row=4, column=3, sticky="ew", padx=5, pady=3)

        tk.Button(
            form,
            text="Programar show",
            command=self.programar_evento,
            bg="#1E4A8C",
            fg="white",
            relief="flat"
        ).grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Cargar show",
            command=self.cargar_evento_en_formulario,
            bg="#7A8AA8",
            fg="white",
            relief="flat"
        ).grid(row=6, column=0, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Actualizar show",
            command=self.actualizar_show,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).grid(row=6, column=1, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Ver detalle show",
            command=self.ver_detalle_evento,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).grid(row=5, column=2, sticky="ew", padx=5, pady=6)

        tk.Button(
            form,
            text="Eliminar show",
            command=self.eliminar_evento,
            bg="#7A8AA8",
            fg="white",
            relief="flat"
        ).grid(row=5, column=3, sticky="ew", padx=5, pady=6)

        for columna in range(4):
            form.grid_columnconfigure(columna, weight=1)

    def limpiar_formulario(self) -> None:
        self.entry_nombre.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

    def obtener_evento_seleccionado(self):
        evento_id = self.seleccionar_evento_id_callback()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show.")
            return None

        evento = self.controller.obtener_evento(evento_id)
        if evento is None:
            messagebox.showerror("Error", "No se encontro el show.")
            return None

        return evento

    def programar_evento(self) -> None:
        try:
            duracion = int(self.entry_duracion.get().strip())
        except ValueError:
            messagebox.showerror("Dato invalido", "La duracion debe ser un numero entero.")
            return

        resultado_programacion = self.controller.programar_evento(
            nombre=self.entry_nombre.get().strip(),
            categoria=self.combo_categoria.get().strip(),
            fecha=self.entry_fecha.get().strip(),
            hora_inicio=self.entry_hora.get().strip(),
            duracion_minutos=duracion,
            descripcion=self.entry_descripcion.get().strip()
        )
        ok = resultado_programacion[0]
        mensaje = resultado_programacion[1]

        if not ok:
            messagebox.showerror("No se pudo programar", mensaje)
            return

        messagebox.showinfo("Exito", mensaje)
        self.limpiar_formulario()
        self.refrescar_eventos_callback()

    def cargar_evento_en_formulario(self) -> None:
        evento = self.obtener_evento_seleccionado()
        if evento is None:
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

        self.cargar_precios_callback(evento)

    def actualizar_show(self) -> None:
        evento_id = self.seleccionar_evento_id_callback()
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
            descripcion=self.entry_descripcion.get().strip()
        )

        if ok:
            messagebox.showinfo("Exito", mensaje)
            self.refrescar_eventos_callback()
        else:
            messagebox.showerror("Error", mensaje)

    def ver_detalle_evento(self) -> None:
        evento = self.obtener_evento_seleccionado()
        if evento is None:
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

    def eliminar_evento(self) -> None:
        evento_id = self.seleccionar_evento_id_callback()
        if evento_id is None:
            messagebox.showwarning("Seleccion requerida", "Selecciona un show.")
            return

        ok, mensaje = self.controller.eliminar_evento(evento_id)
        if ok:
            messagebox.showinfo("Exito", mensaje)
            self.refrescar_eventos_callback()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)
