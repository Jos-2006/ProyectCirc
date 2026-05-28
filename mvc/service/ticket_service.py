from datetime import datetime
from typing import Dict, List, Optional, Tuple

from model.evento import Evento
from model.ticket import Ticket
from repo.evento_repository import EventoRepository
from repo.ticket_repository import TicketRepository


class TicketService:
    """Logica de venta y reportes de boletos."""

    MAPA_ZONAS = {
        "general": "General",
        "preferencial": "Preferencial",
        "vip": "VIP",
    }

    def __init__(
        self,
        ticket_repo: Optional[TicketRepository] = None,
        evento_repo: Optional[EventoRepository] = None,
    ) -> None:
        self.ticket_repo = ticket_repo or TicketRepository()
        self.evento_repo = evento_repo or EventoRepository()

    def _obtener_siguiente_asiento(self, evento_id: int, zona: str, capacidad_zona: int) -> Optional[int]:
        tickets_zona = self.ticket_repo.obtener_por_evento_y_zona(evento_id, zona)
        asientos_ocupados = {ticket.numero_asiento for ticket in tickets_zona}
        for asiento in range(1, capacidad_zona + 1):
            if asiento not in asientos_ocupados:
                return asiento
        return None

    def vender_ticket(
        self,
        evento_id: int,
        zona: str,
        metodo_pago: str,
        usuario_id: Optional[int] = None,
    ) -> Tuple[bool, str, Optional[Ticket]]:
        evento = self.evento_repo.obtener_por_id(evento_id)
        if evento is None:
            return False, "El show seleccionado no existe.", None

        zona_limpia = self.MAPA_ZONAS.get(zona.strip().lower(), "")
        if zona_limpia not in evento.capacidad_por_zona:
            return False, "Zona invalida.", None

        capacidad_zona = evento.capacidad_por_zona[zona_limpia]
        asiento = self._obtener_siguiente_asiento(evento_id, zona_limpia, capacidad_zona)
        if asiento is None:
            return False, "No hay asientos disponibles en esta zona.", None

        precio = float(evento.precios_por_zona.get(zona_limpia, 0.0))
        if precio <= 0:
            return False, "El show no tiene precio configurado para esa zona.", None

        nuevo_id = self.ticket_repo.obtener_ultimo_id() + 1
        ticket = Ticket(
            identificador=nuevo_id,
            evento_id=evento_id,
            usuario_id=usuario_id,
            zona=zona_limpia,
            numero_asiento=asiento,
            precio=precio,
            fecha_compra=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metodo_pago=metodo_pago.strip() or "Sin especificar",
        )
        self.ticket_repo.agregar(ticket)
        return True, "Venta realizada correctamente.", ticket

    def asientos_disponibles(self, evento_id: int) -> Optional[Dict[str, int]]:
        evento = self.evento_repo.obtener_por_id(evento_id)
        if evento is None:
            return None

        disponibles: Dict[str, int] = {}
        for zona, capacidad in evento.capacidad_por_zona.items():
            vendidos = len(self.ticket_repo.obtener_por_evento_y_zona(evento_id, zona))
            disponibles[zona] = capacidad - vendidos
        return disponibles

    def listar_tickets(self) -> List[Ticket]:
        return self.ticket_repo.obtener_todos()

    def tickets_por_evento(self, evento_id: int) -> List[Ticket]:
        return self.ticket_repo.obtener_por_evento(evento_id)

    def tickets_por_usuario(self, usuario_id: int) -> List[Ticket]:
        return self.ticket_repo.obtener_por_usuario(usuario_id)

    def obtener_ticket(self, ticket_id: int) -> Optional[Ticket]:
        return self.ticket_repo.obtener_por_id(ticket_id)

    def evento_tiene_tickets(self, evento_id: int) -> bool:
        return len(self.ticket_repo.obtener_por_evento(evento_id)) > 0

    def reporte_evento(self, evento: Evento) -> dict:
        tickets = self.ticket_repo.obtener_por_evento(evento.identificador)
        resumen = {
            "evento": evento.nombre,
            "categoria": evento.categoria,
            "fecha": evento.fecha,
            "hora_inicio": evento.hora_inicio,
            "por_zona": {},
            "total_vendidos": 0,
            "total_recaudado": 0.0,
            "ocupacion": 0.0,
        }

        capacidad_total = 0
        vendidos_total = 0

        for zona, capacidad in evento.capacidad_por_zona.items():
            tickets_zona = [ticket for ticket in tickets if ticket.zona.lower() == zona.lower()]
            vendidos = len(tickets_zona)
            recaudado = sum(ticket.precio for ticket in tickets_zona)
            disponibles = capacidad - vendidos

            resumen["por_zona"][zona] = {
                "capacidad": capacidad,
                "vendidos": vendidos,
                "disponibles": disponibles,
                "recaudado": recaudado,
            }

            capacidad_total += capacidad
            vendidos_total += vendidos
            resumen["total_recaudado"] += recaudado

        resumen["total_vendidos"] = vendidos_total
        resumen["ocupacion"] = (vendidos_total / capacidad_total * 100) if capacidad_total else 0.0
        return resumen

    def reporte_general(self, eventos: List[Evento]) -> dict:
        total_tickets = 0
        total_recaudado = 0.0
        ocupacion_por_evento: Dict[int, float] = {}
        resumen_por_categoria: Dict[str, int] = {}

        for evento in eventos:
            reporte = self.reporte_evento(evento)
            total_tickets += reporte["total_vendidos"]
            total_recaudado += reporte["total_recaudado"]
            ocupacion_por_evento[evento.identificador] = reporte["ocupacion"]
            categoria = evento.categoria
            resumen_por_categoria[categoria] = resumen_por_categoria.get(categoria, 0) + reporte["total_vendidos"]

        top_evento_id = max(ocupacion_por_evento, key=ocupacion_por_evento.get) if ocupacion_por_evento else None
        return {
            "total_eventos": len(eventos),
            "total_tickets": total_tickets,
            "total_recaudado": total_recaudado,
            "ventas_por_categoria": resumen_por_categoria,
            "evento_top_ocupacion_id": top_evento_id,
            "ocupacion_promedio": (
                sum(ocupacion_por_evento.values()) / len(ocupacion_por_evento)
                if ocupacion_por_evento
                else 0.0
            ),
        }

    def reporte_por_fecha(self, fecha: str, eventos: List[Evento]) -> dict:
        eventos_filtrados = [evento for evento in eventos if evento.fecha == fecha]
        reporte_base = self.reporte_general(eventos_filtrados)
        reporte_base["fecha_consultada"] = fecha
        return reporte_base

