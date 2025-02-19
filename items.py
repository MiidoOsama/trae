from pydantic import BaseModel
from uuid import UUID , uuid1 , uuid3 , uuid4 , uuid5

class Item(BaseModel):
    id : UUID = uuid4()
    name: str
    description: str | None = None
    price: float
    tax: float | None = None