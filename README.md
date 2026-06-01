# ProyectCirc

Sistema de boleteria y gestion de shows para un circo, desarrollado en Python con arquitectura MVC, persistencia en JSON y GUI modular con Tkinter.

## Objetivo del proyecto

Resolver problemas operativos del circo:

- choques de horarios entre funciones
- sobreventa por control manual del aforo
- poca trazabilidad de ventas y recaudacion

## Arquitectura implementada

Estructura usada (segun lo solicitado):

```text
ProyectCirc/
├── mvc/
│   ├── controller/
│   ├── model/
│   ├── view/
│   ├── repo/
│   ├── service/
│   ├── data/
│   └── main.py
└── README.md
```

### Capas

- `mvc/model`: entidades `Usuario`, `Evento`, `Ticket`.
- `mvc/repo`: persistencia JSON por entidad (`usuarios.json`, `eventos.json`, `tickets.json`).
- `mvc/service`: logica de negocio (validaciones, horarios, aforo, ventas, reportes).
- `mvc/controller`: coordinacion entre GUI y servicios.
- `mvc/view`: interfaz grafica modular por rol (`Login`, `Admin`, `Cliente`, `Boleteria`).
- `mvc/main.py`: punto de entrada y enrutamiento por rol.

## Funcionalidades principales

### 1. Login y control de acceso

- inicio de sesion por rol: `Administrador`, `Cajero`, `Cliente`
- registro de clientes desde GUI
- acceso restringido a funcionalidades segun rol

Credenciales demo:

- Admin: `admin@circo.com / admin123`
- Cajero: `cajero@circo.com / cajero123`
- Cliente: `cliente@circo.com / cliente123`

### 2. Modulos funcionales

- **Administrador**
  - registrar shows
  - consulta individual de show
  - listado en tabla
  - eliminar show (si no tiene ventas)
  - actualizar precios por zona
  - cargar shows demo

- **Cliente**
  - cartelera digital
  - consulta individual de show
  - compra de entradas por zona
  - visualizacion de asientos disponibles
  - historial de tickets del cliente

- **Boleteria (Cajero)**
  - listado de shows
  - consulta individual de show
  - venta rapida en taquilla
  - disponibilidad en tiempo real

### 3. Procesos de negocio (Service)

- validacion de credenciales y reglas de registro
- validacion de fecha/hora de shows
- deteccion de choque de horarios
- control de aforo por zona (VIP/Preferencial/General)
- asignacion automatica de asiento
- calculo de precios y recaudacion

### 4. Reportes en GUI

- reporte por show (ventas por zona, ocupacion, recaudacion)
- reporte general (totales, categoria mas vendida, top ocupacion)
- reporte filtrado por fecha
- consulta individual de ticket por ID

## Persistencia JSON

- almacenamiento en archivos separados por entidad
- carga automatica al iniciar
- guardado automatico al registrar/actualizar datos

## Evidencia de SOLID y buenas practicas

- **Single Responsibility**: cada capa tiene responsabilidad unica.
- **Open/Closed (parcial)**: servicios listos para extender reglas sin tocar GUI.
- **Dependency Inversion (basico)**: controladores dependen de servicios, no de JSON directo.
- bajo acoplamiento y sin mezclar logica de negocio en vistas.

## Estructuras de datos usadas

- listas: colecciones de eventos, tickets y usuarios
- diccionarios: precios/capacidades y reportes
- tuplas: ventanas de tiempo para validar choques
- conjuntos: asientos ocupados y control de duplicados en carga demo

## Ejecucion

Requisito: Python 3.10+.

```bash
python mvc/main.py
```

## Restricciones cumplidas

- sin frameworks externos de GUI
- sin clase gigante unica
- sin mezclar logica de negocio con interfaz
- sin duplicacion innecesaria de logica

## Matriz de evaluacion del entregable

- **Funcionalidad del sistema (3%)**: login por roles, venta de tickets, control de aforo y reportes.
- **Arquitectura MVC (2%)**: separacion en `model`, `repo`, `service`, `controller` y `view`.
- **Principios SOLID (2%)**: responsabilidades separadas por capa y componentes de GUI modulares.
- **GUI modular (1.5%)**: vistas separadas por rol y modulos de administrador divididos por panel.
- **Persistencia JSON (1%)**: almacenamiento por entidad en `mvc/data`.
- **GitHub y commits (0.5%)**: historial de commits por bloques funcionales.

## Nota sobre commits

Durante el desarrollo se utilizo una convencion de mensajes de commit para documentar de forma clara y ordenada los cambios del proyecto, tal como se practica en proyectos de mayor alcance.
