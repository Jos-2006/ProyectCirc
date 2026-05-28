from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class Evento:
    """Entidad de show/funcion del circo."""

    identificador: int
    nombre: str
    categoria: str
    fecha: str
    hora_inicio: str
    duracion_minutos: int
    descripcion: str
    precios_por_zona: Dict[str, float]
    capacidad_por_zona: Dict[str, int]

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Evento":
        return Evento(
            identificador=int(data.get("identificador", 0)),
            nombre=data.get("nombre", "").strip(),
            categoria=data.get("categoria", "General").strip() or "General",
            fecha=data.get("fecha", "").strip(),
            hora_inicio=data.get("hora_inicio", "").strip(),
            duracion_minutos=int(data.get("duracion_minutos", 0)),
            descripcion=data.get("descripcion", "").strip(),
            precios_por_zona=dict(data.get("precios_por_zona", {})),
            capacidad_por_zona=dict(data.get("capacidad_por_zona", {})),
        )
