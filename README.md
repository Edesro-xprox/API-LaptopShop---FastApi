
# LaptopShopper API

API backend para gestión de laptops usando FastAPI y SQLAlchemy.

## Requisitos
- Python 3.10+
- SQL Server y ODBC Driver 17+ (solo si usas base de datos)

## Instalación rápida
1. Crea y activa un entorno virtual:
	```bash
	python -m venv .venv
	.venv\Scripts\activate
	```
2. Instala dependencias:
	```bash
	pip install -r requirements.txt
	```
3. Copia `.env.example` a `.env` y configura la cadena de conexión si usarás SQL Server.

## Uso
Inicia el servidor de desarrollo:
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints principales
- `GET /api/laptops` : Lista de laptops (de ejemplo o desde base de datos)
- `POST /api/laptops` : Crear laptop
- `PUT /api/laptops/{laptop_id}/{quantity}` : Actualizar cantidad
- `DELETE /api/laptops/{laptop_id}` : Eliminar por id
- `DELETE /api/laptops` : Eliminar todos

## Notas
- Si la base de datos no está configurada, se usan datos de ejemplo.
- El modelo y la sesión SQLAlchemy están en `app/models/laptop.py` y `app/db/session.py`.

---
Proyecto minimalista, ideal para aprender FastAPI y SQLAlchemy.

