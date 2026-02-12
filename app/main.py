from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.cart import router as cart_router
from app.core.config import settings

main = FastAPI(title="LaptopShopper API")

origins = [settings.origins]

main.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Orígenes permitidos
    allow_credentials=True,         # Permitir cookies / auth headers
    allow_methods=["*"],            # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],            # Headers permitidos
)
main.include_router(cart_router, prefix="/api")

@main.get("/", include_in_schema=False)
async def root_redirect():
    return {"message": "Use /api/ as base route. Try /api/laptops"}
