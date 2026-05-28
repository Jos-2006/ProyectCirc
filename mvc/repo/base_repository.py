import json
from pathlib import Path
from typing import Generic, List, Optional, Type, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Repositorio base para persistencia JSON."""

    def __init__(self, archivo_json: Path, modelo_cls: Type[T]) -> None:
        self.archivo_json = archivo_json
        self.modelo_cls = modelo_cls
        self.archivo_json.parent.mkdir(parents=True, exist_ok=True)
        if not self.archivo_json.exists():
            self.archivo_json.write_text("[]", encoding="utf-8")

    def _leer(self) -> List[T]:
        try:
            contenido = self.archivo_json.read_text(encoding="utf-8-sig").strip()
            if not contenido:
                return []
            data = json.loads(contenido)
            if not isinstance(data, list):
                return []
        except (json.JSONDecodeError, OSError):
            return []

        resultado: List[T] = []
        for item in data:
            if isinstance(item, dict):
                resultado.append(self.modelo_cls.from_dict(item))
        return resultado

    def _escribir(self, objetos: List[T]) -> None:
        datos = [obj.to_dict() for obj in objetos]
        self.archivo_json.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def obtener_todos(self) -> List[T]:
        return self._leer()

    def obtener_por_id(self, identificador: int) -> Optional[T]:
        for entidad in self._leer():
            if getattr(entidad, "identificador", None) == identificador:
                return entidad
        return None

    def agregar(self, objeto: T) -> T:
        entidades = self._leer()
        entidades.append(objeto)
        self._escribir(entidades)
        return objeto

    def actualizar(self, objeto: T) -> bool:
        entidades = self._leer()
        for index, actual in enumerate(entidades):
            if getattr(actual, "identificador", None) == getattr(objeto, "identificador", None):
                entidades[index] = objeto
                self._escribir(entidades)
                return True
        return False

    def eliminar(self, identificador: int) -> bool:
        entidades = self._leer()
        filtradas = [entidad for entidad in entidades if getattr(entidad, "identificador", None) != identificador]
        if len(filtradas) == len(entidades):
            return False
        self._escribir(filtradas)
        return True


