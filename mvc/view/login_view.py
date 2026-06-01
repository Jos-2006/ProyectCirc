import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from controller.auth_controller import AuthController


class LoginView:
    def __init__(self, root: tk.Tk, on_login: Callable[[str, int], None]) -> None:
        self.root = root
        self.on_login = on_login
        self.auth_controller = AuthController()
        self._construir_gui()

    def _construir_gui(self) -> None:
        self.root.title("Sistema de Circo - Login")
        self.root.configure(bg="#EEF3FF")

        card = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=380)

        tk.Label(
            card,
            text="ProyectCirc",
            bg="white",
            fg="#1E4A8C",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(24, 4))

        tk.Label(
            card,
            text="Boleteria y gestion de shows",
            bg="white",
            fg="#445",
            font=("Segoe UI", 11)
        ).pack(pady=(0, 20))

        tk.Label(card, text="Correo", bg="white", anchor="w").pack(fill="x", padx=34)
        self.entry_correo = tk.Entry(card, font=("Segoe UI", 10))
        self.entry_correo.pack(fill="x", padx=34, pady=(0, 10))

        tk.Label(card, text="Contrasena", bg="white", anchor="w").pack(fill="x", padx=34)
        self.entry_contrasena = tk.Entry(card, show="*", font=("Segoe UI", 10))
        self.entry_contrasena.pack(fill="x", padx=34, pady=(0, 18))

        tk.Button(
            card,
            text="Iniciar sesion",
            bg="#1E4A8C",
            fg="white",
            relief="flat",
            command=self._login,
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x", padx=34, pady=(0, 8))

        tk.Button(
            card,
            text="Crear cuenta cliente",
            bg="#4E7AC7",
            fg="white",
            relief="flat",
            command=self._abrir_registro,
            font=("Segoe UI", 10)
        ).pack(fill="x", padx=34)

        credenciales_info = (
            "Admin: admin@circo.com / admin123\n"
            "Cajero: cajero@circo.com / cajero123\n"
            "Cliente demo: cliente@circo.com / cliente123"
        )
        tk.Label(
            card,
            text=credenciales_info,
            bg="white",
            fg="#667",
            justify="left",
            font=("Consolas", 9)
        ).pack(pady=(16, 0))

    def _login(self) -> None:
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not correo or not contrasena:
            messagebox.showwarning("Campos requeridos", "Completa correo y contrasena.")
            return

        usuario = self.auth_controller.iniciar_sesion(correo, contrasena)
        if usuario is None:
            messagebox.showerror("Acceso denegado", "Credenciales invalidas.")
            return

        messagebox.showinfo("Bienvenido", f"Ingreso correcto: {usuario.nombre_completo}")
        self.on_login(usuario.rol, usuario.identificador)

    def _abrir_registro(self) -> None:
        ventana = tk.Toplevel(self.root)
        RegistroView(ventana, self.auth_controller)


class RegistroView:
    def __init__(self, ventana: tk.Toplevel, auth_controller: AuthController) -> None:
        self.ventana = ventana
        self.auth_controller = auth_controller
        self._construir_gui()

    def _construir_gui(self) -> None:
        self.ventana.title("Registro de cliente")
        self.ventana.geometry("430x330")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#EEF3FF")

        card = tk.Frame(self.ventana, bg="white", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=390, height=290)

        tk.Label(
            card,
            text="Crear cuenta",
            bg="white",
            fg="#1E4A8C",
            font=("Segoe UI", 19, "bold")
        ).pack(pady=(14, 10))

        tk.Label(card, text="Nombre completo", bg="white", anchor="w").pack(fill="x", padx=28)
        self.entry_nombre = tk.Entry(card)
        self.entry_nombre.pack(fill="x", padx=28, pady=(0, 8))

        tk.Label(card, text="Correo", bg="white", anchor="w").pack(fill="x", padx=28)
        self.entry_correo = tk.Entry(card)
        self.entry_correo.pack(fill="x", padx=28, pady=(0, 8))

        tk.Label(card, text="Contrasena (min 4)", bg="white", anchor="w").pack(fill="x", padx=28)
        self.entry_contrasena = tk.Entry(card, show="*")
        self.entry_contrasena.pack(fill="x", padx=28, pady=(0, 14))

        tk.Button(
            card,
            text="Registrar",
            bg="#1E4A8C",
            fg="white",
            relief="flat",
            command=self._registrar
        ).pack(fill="x", padx=28, pady=(0, 6))

        tk.Button(
            card,
            text="Cancelar",
            bg="#9BAECE",
            fg="white",
            relief="flat",
            command=self.ventana.destroy
        ).pack(fill="x", padx=28)

    def _registrar(self) -> None:
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not nombre or not correo or not contrasena:
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return

        usuario = self.auth_controller.registrar(nombre, correo, contrasena, rol="Cliente")
        if usuario is None:
            messagebox.showerror(
                "No se pudo registrar",
                "Revisa correo, contrasena (min 4) o si el correo ya existe."
            )
            return

        messagebox.showinfo("Registro exitoso", "Tu cuenta fue creada correctamente.")
        self.ventana.destroy()

