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

    # return SAMPLE_LAPTOPS

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