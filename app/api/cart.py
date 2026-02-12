from fastapi import APIRouter, HTTPException, status
from typing import List

from sqlalchemy import text
from app.schemas.laptop import LaptopType

from app.db.session import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from app.models.laptop import Laptop as LaptopModel
from app.models.cart import Cart as CartModel

router = APIRouter()

@router.get("/", tags=["base"])
async def api_base():
    return {"message": "LaptopShopper API base. Use /api/laptops to fetch data."}



# --- Datos de ejemplo ---
SAMPLE_LAPTOPS = [
    {"iLaptopId": 1, "name": "Acer Aspire 5", "image": "laptop_01", "description": "Rendimiento equilibrado para tareas cotidianas y productividad.", "price": 750},
    {"iLaptopId": 2, "name": "Dell Inspiron 14", "image": "laptop_02", "description": "Diseño compacto con buena autonomía ideal para estudiantes.", "price": 820},
    {"iLaptopId": 3, "name": "HP Pavilion X360", "image": "laptop_03", "description": "Convertible 2 en 1 con pantalla táctil y excelente versatilidad.", "price": 890},
    {"iLaptopId": 4, "name": "Lenovo IdeaPad 5", "image": "laptop_04", "description": "Ligera y potente, ideal para multitarea y uso prolongado.", "price": 910},
    {"iLaptopId": 5, "name": "Asus VivoBook S15", "image": "laptop_05", "description": "Pantalla amplia y colores vibrantes para una experiencia multimedia.", "price": 950},
    {"iLaptopId": 6, "name": "MacBook Air M1", "image": "laptop_06", "description": "Eficiencia sobresaliente y rendimiento silencioso con chip Apple.", "price": 1200},
    {"iLaptopId": 7, "name": "MacBook Pro M2", "image": "laptop_07", "description": "Potencia profesional con excelente duración de batería.", "price": 1800},
    {"iLaptopId": 8, "name": "MSI Modern 14", "image": "laptop_08", "description": "Ideal para productividad y diseño liviano con buen rendimiento.", "price": 1050},
    {"iLaptopId": 9, "name": "Razer Blade 15", "image": "laptop_09", "description": "Laptop gamer premium con construcción sólida y gráficos potentes.", "price": 2200},
    {"iLaptopId": 10, "name": "Acer Nitro 5", "image": "laptop_10", "description": "Perfecta para gaming casual y tareas pesadas a buen precio.", "price": 1100},
    {"iLaptopId": 11, "name": "ASUS TUF Gaming F15", "image": "laptop_11", "description": "Diseñada para rendimiento exigente y durabilidad extrema.", "price": 1300},
    {"iLaptopId": 12, "name": "Samsung Galaxy Book Pro", "image": "laptop_12", "description": "Ultraliviana y eficiente, perfecta para movilidad y productividad.", "price": 1400}
]

@router.get("/laptops", response_model=List[LaptopType], tags=["laptops"])
async def get_laptops():
    # Intenta obtener desde la base de datos; si falla, retorna datos de ejemplo.
    db = None
    try:
        db = SessionLocal()
        laptops = db.query(LaptopModel).all()
        if laptops:
            return laptops
    except SQLAlchemyError:
        # Si hay problema con la conexión/consulta, caemos al fallback
        pass
    finally:
        if db:
            db.close()

    # Devuelve datos de ejemplo si no hay conexión o no hay datos
    return SAMPLE_LAPTOPS

@router.get("/cart", tags=["cart"])
async def get_cart():
    # Intenta obtener desde la base de datos; si falla, retorna datos de ejemplo.
    db = None
    try:
        db = SessionLocal()
        cart = db.query(CartModel).all()
        if cart:
            return cart
    except SQLAlchemyError:
        # Si hay problema con la conexión/consulta, caemos al fallback
        pass
    finally:
        if db:
            db.close()


@router.post("/cart/{laptop_id}", status_code=status.HTTP_201_CREATED, tags=["cart"])
async def add_cart(laptop_id: int):
    # Crea un registro en la DB usando los campos del objeto; si la DB falla, lanza error.
    db = None
    try:
        db = SessionLocal()
        result = db.execute(
            text("""
                EXEC spi_addToCart
                    @iLaptopId = :laptop_id
            """),
            {
                "laptop_id": laptop_id
            }
        )
        res = result.fetchone()
        db.commit()
        return {"message": "Laptop added to cart"}
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if db:
            db.close()


@router.delete("/cart/{laptop_id}", tags=["cart"])
async def remove_cart(laptop_id: int):
    # Elimina un registro por id
    db = None
    try:
        db = SessionLocal()
        result = db.execute(
            text("""
                EXEC spd_removeFromCart
                    @iLaptopId = :laptop_id
            """),
            {
                "laptop_id": laptop_id
            }
        )
        result.fetchone()
        db.commit()
        return {"message": "Laptop removed from cart"}
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if db:
            db.close()


@router.put("/cart/{laptop_id}/{value}", tags=["cart"])
async def update_laptop_quantity(laptop_id: int, value: int):
    # Actualiza solo la cantidad de un laptop por id
    db = None
    try:
        db = SessionLocal()
        result = db.execute(
            text("""
                EXEC spu_updateCartQuantity
                    @iLaptopId = :laptop_id,
                    @value = :value
            """),
            {
                "laptop_id": laptop_id,
                "value": value
            }
        )
        result.fetchone()
        db.commit()
        return {"message": "Laptop quantity updated in cart"}
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if db:
            db.close()


@router.delete("/cart", tags=["cart"])
async def delete_all_cart_items():
    # Elimina todos los registros de la tabla cart
    db = None
    try:
        db = SessionLocal()
        result = db.execute(
            text("""
                EXEC spd_clearCart
            """)
        )
        result.fetchone()
        db.commit()
        return {"message": "All items removed from cart"}
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if db:
            db.close()