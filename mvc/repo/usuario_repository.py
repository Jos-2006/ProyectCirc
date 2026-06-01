from pathlib import Path
from typing import Optional

from model.usuario import Usuario
from repo.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, archivo_json: Optional[Path] = None) -> None:
        ruta = archivo_json or (Path(__file__).resolve().parent.parent / "data" / "usuarios.json")
        super().__init__(ruta, Usuario)

    def obtener_por_correo(self, correo_electronico: str) -> Optional[Usuario]:
        correo_buscado = correo_electronico.strip().lower()
        for usuario in self.get_all():
            if usuario.correo_electronico.lower() == correo_buscado:
                return usuario
        return None

    def obtener_ultimo_id(self) -> int:
        ultimo_id = 0
        for usuario in self.get_all():
            if usuario.identificador > ultimo_id:
                ultimo_id = usuario.identificador
        return ultimo_id

