from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_utils import get_db
from app.models import Customer, Item
from app.schemas import CustomerCreate, ItemCreate


class CustomerService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, customer: CustomerCreate) -> Customer:
        db_customer = Customer(**customer.model_dump())
        self.db.add(db_customer)
        await self.db.commit()
        await self.db.refresh(db_customer)
        return db_customer

    async def get(self, customer_id: int) -> Optional[Customer]:
        result = await self.db.execute(
            select(Customer).filter(Customer.id == customer_id)
        )
        return result.scalars().first()


class ItemService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, item: ItemCreate) -> Item:
        db_item = Item(**item.model_dump())
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def get_all(self) -> List[Item]:
        result = await self.db.execute(select(Item))
        return result.scalars().all()
