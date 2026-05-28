from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Usuario:
    """Entidad de usuario del sistema."""

    identificador: int
    nombre_completo: str
    correo_electronico: str
    contrasena: str
    rol: str
    direccion: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Usuario":
        return Usuario(
            identificador=int(data.get("identificador", 0)),
            nombre_completo=data.get("nombre_completo", "").strip(),
            correo_electronico=data.get("correo_electronico", "").strip(),
            contrasena=data.get("contrasena", ""),
            rol=data.get("rol", "Cliente"),
            direccion=data.get("direccion"),
        )

