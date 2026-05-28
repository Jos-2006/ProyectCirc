from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Ticket:
    """Entidad de ticket vendido."""

    identificador: int
    evento_id: int
    usuario_id: Optional[int]
    zona: str
    numero_asiento: int
    precio: float
    fecha_compra: str
    metodo_pago: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Ticket":
        return Ticket(
            identificador=int(data.get("identificador", 0)),
            evento_id=int(data.get("evento_id", 0)),
            usuario_id=(int(data["usuario_id"]) if data.get("usuario_id") is not None else None),
            zona=data.get("zona", "General"),
            numero_asiento=int(data.get("numero_asiento", 0)),
            precio=float(data.get("precio", 0.0)),
            fecha_compra=data.get("fecha_compra", ""),
            metodo_pago=data.get("metodo_pago", "Sin especificar"),
        )

