from pathlib import Path
from typing import List, Optional

from model.ticket import Ticket
from repo.base_repository import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, archivo_json: Optional[Path] = None) -> None:
        ruta = archivo_json or (Path(__file__).resolve().parent.parent / "data" / "tickets.json")
        super().__init__(ruta, Ticket)

    def obtener_ultimo_id(self) -> int:
        tickets = self.get_all()
        return max((ticket.identificador for ticket in tickets), default=0)

    def obtener_por_evento(self, evento_id: int) -> List[Ticket]:
        return [ticket for ticket in self.get_all() if ticket.evento_id == evento_id]

    def obtener_por_evento_y_zona(self, evento_id: int, zona: str) -> List[Ticket]:
        zona_buscada = zona.strip().lower()
        return [
            ticket
            for ticket in self.get_all()
            if ticket.evento_id == evento_id and ticket.zona.lower() == zona_buscada
        ]

    def obtener_por_usuario(self, usuario_id: int) -> List[Ticket]:
        return [ticket for ticket in self.get_all() if ticket.usuario_id == usuario_id]

    def obtener_por_zona(self, zona: str) -> List[Ticket]:
        zona_buscada = zona.strip().lower()
        return [ticket for ticket in self.get_all() if ticket.zona.lower() == zona_buscada]

