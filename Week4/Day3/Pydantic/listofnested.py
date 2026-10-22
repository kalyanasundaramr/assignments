
from pydantic import BaseModel

# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: Nested models allow for complex data structures. Here, the Order model contains a list of Item models as a field.
class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    order_id: int
    items: list[Item]

order = Order(
    order_id=1001,
    items=[
        {"name": "Laptop", "price": 50000},
        {"name": "Mouse", "price": 800},
        {"name": "Keyboard", "price": 1500}
    ]
)

print("Order ID:", order.order_id)

for item in order.items:
    print(item.name, "-", item.price)
