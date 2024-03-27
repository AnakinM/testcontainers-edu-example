from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    age: int


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    name: str
    description: str
    price: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
