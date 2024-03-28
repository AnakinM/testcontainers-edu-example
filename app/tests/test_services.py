import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CustomerCreate, ItemCreate
from app.services import CustomerService, ItemService


pytestmark = pytest.mark.asyncio
# Unit tests


@pytest.mark.usefixtures("event_loop")
async def test_create_customer(async_db: AsyncSession, sample_customer: CustomerCreate):
    customer_service = CustomerService(db=async_db)
    customer = await customer_service.create(sample_customer)
    assert customer.id == 1
    assert customer.first_name == sample_customer.first_name
    assert customer.last_name == sample_customer.last_name
    assert customer.age == sample_customer.age


@pytest.mark.usefixtures("event_loop")
async def test_get_customer(async_db: AsyncSession, sample_customer: CustomerCreate):
    customer_service = CustomerService(db=async_db)
    customer = await customer_service.get(1)
    assert customer.id == 1
    assert customer.first_name == sample_customer.first_name
    assert customer.last_name == sample_customer.last_name
    assert customer.age == sample_customer.age


@pytest.mark.usefixtures("event_loop")
async def test_create_item(async_db: AsyncSession, sample_item: ItemCreate):
    item_service = ItemService(db=async_db)
    item = await item_service.create(sample_item)
    assert item.id == 1
    assert item.name == sample_item.name
    assert item.description == sample_item.description
    assert item.price == sample_item.price


@pytest.mark.usefixtures("event_loop")
async def test_list_items(async_db: AsyncSession, sample_item: ItemCreate):
    item_service = ItemService(db=async_db)
    items = await item_service.get_all()
    assert len(items) == 1
    assert items[0].id == 1
    assert items[0].name == sample_item.name
    assert items[0].description == sample_item.description
    assert items[0].price == sample_item.price
