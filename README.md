# LaptopShopper API (FastAPI)

Proyecto backend mínimo con FastAPI, arquitectura por capas y rutas básicas.

Requisitos:
- Python 3.10+
- ODBC Driver for SQL Server (Windows): "ODBC Driver 17 for SQL Server" o superior

Instalación:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Variables de entorno:
- Crea un archivo `.env` a partir de `.env.example` y configura tu cadena de conexión SQL Server en `SQLALCHEMY_DATABASE_URL`.

Ejecutar servidor de desarrollo:

```bash
uvicorn app.main:app --reload --port 8000
```

Rutas principales:
- `GET /api/` : Ruta base
- `GET /api/laptops` : Obtiene lista completa (datos de ejemplo estáticos)
- `POST /api/laptops` : Crear (función vacía)
- `DELETE /api/laptops/{laptop_id}` : Eliminar por id (función vacía)
- `PUT /api/laptops/{laptop_id}/{quantity}` : Actualizar con 2 parámetros (función vacía)
- `DELETE /api/laptops` : Eliminar todo (función vacía)

Notas:
- He dejado las funciones POST/PUT/DELETE vacías tal como pediste para que implementes la lógica de negocio.
- Si quieres que los endpoints usen la base de datos SQL Server ahora, dime y puedo añadir ejemplo con SQLAlchemy.

DB integration notes:
- The project includes an ORM model at `app/models/laptop.py` and a SQLAlchemy session in `app/db/session.py`.
- `GET /api/laptops` will try to read from SQL Server if `SQLALCHEMY_DATABASE_URL` in `.env` is configured; otherwise it returns the example dataset.
- To create the `laptops` table manually you can run a simple script (example below) once your SQL Server is ready.

Quick create-table example (run after configuring `.env`):

```python
from app.db.session import engine
from app.models.laptop import Base

Base.metadata.create_all(bind=engine)
```

CRUD implemented:
- `POST /api/laptops` : crea un laptop (requiere objeto con `id`, `name`, `price`, etc.). Falla si ya existe el `id`.
- `DELETE /api/laptops/{laptop_id}` : elimina un laptop por `id`.
- `PUT /api/laptops/{laptop_id}/{quantity}` : actualiza solo la `quantity` del laptop.
- `DELETE /api/laptops` : elimina todos los registros y devuelve el conteo eliminado.

Notas:
- Las rutas ahora usan SQLAlchemy y retornan errores HTTP adecuados cuando hay conflictos o recursos no encontrados.
- Si la base de datos no está disponible, `GET /api/laptops` seguirá devolviendo los datos de ejemplo.

