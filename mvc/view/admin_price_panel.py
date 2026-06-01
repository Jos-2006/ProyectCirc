import tkinter as tk
from tkinter import messagebox


class AdminPricePanel:
    """Panel de gestion de precios y asientos."""

    def __init__(
        self,
        parent,
        controller,
        seleccionar_evento_id_callback,
        refrescar_eventos_callback
    ) -> None:
        self.controller = controller
        self.seleccionar_evento_id_callback = seleccionar_evento_id_callback
        self.refrescar_eventos_callback = refrescar_eventos_callback
        self.crear_panel(parent)

    def crear_panel(self, parent) -> None:
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=14, pady=(0, 6))

        tk.Label(
            frame,
            text="Gestion de precios por zona",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=7, sticky="w", padx=5, pady=(0, 4))

        tk.Label(frame, text="General", bg="white").grid(row=1, column=0, padx=5, pady=4)
        self.entry_precio_general = tk.Entry(frame, width=10)
        self.entry_precio_general.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame, text="Preferencial", bg="white").grid(row=1, column=2, padx=5, pady=4)
        self.entry_precio_preferencial = tk.Entry(frame, width=10)
        self.entry_precio_preferencial.grid(row=1, column=3, padx=5, pady=4)

        tk.Label(frame, text="VIP", bg="white").grid(row=1, column=4, padx=5, pady=4)
        self.entry_precio_vip = tk.Entry(frame, width=10)
        self.entry_precio_vip.grid(row=1, column=5, padx=5, pady=4)

        tk.Button(
            frame,
            text="Actualizar precios show seleccionado",
            command=self.actualizar_precios,
            bg="#4E7AC7",
            fg="white",
            relief="flat"
        ).grid(row=1, column=6, padx=8, pady=4)

        tk.Label(frame, text="+ General", bg="white").grid(row=2, column=0, padx=5, pady=4)
        self.entry_mas_general = tk.Entry(frame, width=10)
        self.entry_mas_general.grid(row=2, column=1, padx=5, pady=4)

        tk.Label(frame, text="+ Preferencial", bg="white").grid(row=2, column=2, padx=5, pady=4)
        self.entry_mas_preferencial = tk.Entry(frame, width=10)
        self.entry_mas_preferencial.grid(row=2, column=3, padx=5, pady=4)

        tk.Label(frame, text="+ VIP", bg="white").grid(row=2, column=4, padx=5, pady=4)
        self.entry_mas_vip = tk.Entry(frame, width=10)
        self.entry_mas_vip.grid(row=2, column=5, padx=5, pady=4)

        tk.Button(
            frame,
            text="Agregar asientos",
            command=self.agregar_asientos,
            bg="#1E4A8C",
            fg="white",
            relief="flat"
        ).grid(row=2, column=6, padx=8, pady=4)

    def cargar_precios_evento(self, evento) -> None:
        self.entry_precio_general.delete(0, tk.END)
        self.entry_precio_general.insert(0, str(int(evento.precios_por_zona.get("General", 0))))
        self.entry_precio_preferencial.delete(0, tk.END)
        self.entry_precio_preferencial.insert(0, str(int(evento.precios_por_zona.get("Preferencial", 0))))
        self.entry_precio_vip.delete(0, tk.END)
        self.entry_precio_vip.insert(0, str(int(evento.precios_por_zona.get("VIP", 0))))

    def actualizar_precios(self) -> None:
        evento_id = self.seleccionar_evento_id_callback()
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
            self.refrescar_eventos_callback()
        else:
            messagebox.showerror("Error", mensaje)

    def agregar_asientos(self) -> None:
        evento_id = self.seleccionar_evento_id_callback()
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
            agregar_vip=vip
        )

        if ok:
            messagebox.showinfo("Exito", mensaje)
            self.entry_mas_general.delete(0, tk.END)
            self.entry_mas_preferencial.delete(0, tk.END)
            self.entry_mas_vip.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)
