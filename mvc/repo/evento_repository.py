from pathlib import Path
from typing import List, Optional

from model.evento import Evento
from repo.base_repository import BaseRepository


class EventoRepository(BaseRepository[Evento]):
    def __init__(self, archivo_json: Optional[Path] = None) -> None:
        ruta = archivo_json or (Path(__file__).resolve().parent.parent / "data" / "eventos.json")
        super().__init__(ruta, Evento)

    def obtener_por_fecha(self, fecha: str) -> List[Evento]:
        return [evento for evento in self._leer() if evento.fecha == fecha]

    def obtener_por_nombre(self, nombre: str) -> Optional[Evento]:
        nombre_buscado = nombre.strip().lower()
        for evento in self._leer():
            if evento.nombre.lower() == nombre_buscado:
                return evento
        return None

    def obtener_ultimo_id(self) -> int:
        eventos = self._leer()
        return max((evento.identificador for evento in eventos), default=0)

