from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI, status

from app.models import Base
from app.schemas import (
    Customer as CustomerSchema,
    Item as ItemSchema,
    CustomerCreate,
    ItemCreate,
)
from app.services import CustomerService, ItemService
from app.db_utils import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/customers/", response_model=CustomerSchema, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    customer: CustomerCreate, customer_service: CustomerService = Depends()
):
    return await customer_service.create(customer)


@app.get("/customers/{customer_id}", response_model=CustomerSchema)
async def get_customer(customer_id: int, customer_service: CustomerService = Depends()):
    return await customer_service.get(customer_id)


@app.post("/items/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, item_service: ItemService = Depends()):
    return await item_service.create(item)


@app.get("/items/", response_model=List[ItemSchema])
async def list_items(item_service: ItemService = Depends()):
    return await item_service.get_all()
