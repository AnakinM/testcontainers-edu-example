from typing import List
from fastapi import Depends, FastAPI, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Customer, Item
from app.schemas import (
    Customer as CustomerSchema,
    Item as ItemSchema,
    CustomerCreate,
    ItemCreate,
)
from .db_utils import create_tables, get_db, engine


app = FastAPI()
create_tables(engine)


@app.post(
    "/customers/", response_model=CustomerSchema, status_code=status.HTTP_201_CREATED
)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    return None


@app.get("/customers/{customer_id}", response_model=CustomerSchema)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    return result.scalars().first()


@app.post("/items/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    return None


@app.get("/items/", response_model=List[ItemSchema])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()
