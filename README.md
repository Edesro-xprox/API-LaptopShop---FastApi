# Proyecto

LAPTOPSHOPPER_API

# Descripción

Proyecto backend realizado con el framework FastApi para atender las peticiones del usuario.

## Requisitos
- Python 3.14+
- SQL Server y ODBC Driver 17+
- Entorno virtual (venv)

## Tecnología / versión

- FastAPI 0.128.2
- Uvicorn 0.40.0
- SQLAlchemy 2.0.46
- pyodbc 5.3.0
- python-dotenv 1.2.1
- pydantic 2.12.5
- pydantic-settings 2.12.0

## Como ejecutar
- Crea un entorno virtual: python -m venv .venv
- Activa el entorno virtual: .venv\Scripts\activate
- Instala dependencias: pip install -r requirements.txt
- Copia `.env.example` a `.env` y configura la cadena de conexión para SQL Server.
- Inicia el servidor de desarrollo: uvicorn app.main:app --reload --port 8000

## Notas
- Si la base de datos no está configurada, se usan datos de ejemplo pero solo se podrá realizar peticiones tipo GET.

## Autor

Edson Espinoza