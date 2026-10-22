
from pydantic import BaseModel
from typing import Optional


# 1. User model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int


print("User class defined successfully.")

user = User(
    id=1,
    name="John Doe",
    email="john.doe@example.com",
    age=30
)
print(f"User created: {user.name}, {user.email}, {user.age}")


# 2. Pydantic validation example
user2 = User(
    id=2,
    name="Jane Smith",
    email="jane.smith@example.com",
    age="25"
)
print(f"User created: {user2.name}, {user2.email}, {user2.age}")

try:
    user3 = User(
        id=3,
        name="Alex",
        email="alex@example.com",
        age="hello"
    )
except Exception as e:
    print(f"Validation error: {e}")


# 3. Product model with default and optional fields
class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True
    discount: Optional[float] = None


p = Product(id=1, name="Laptop", price=999.99)

print(
    f"Product created: {p.name}, {p.price}, "
    f"In stock: {p.in_stock}, Discount: {p.discount}"
)


# 4. Nested Pydantic models
class Address(BaseModel):
    city: str
    pincode: str


class Person(BaseModel):
    name: str
    address: Address  # A model inside another model


person = Person(
    name="Meera",
    address={
        "city": "Chennai",
        "pincode": "600001"
    }
)

print("\nPerson details:")
print(person)
print("City:", person.address.city)
print("Pincode:", person.address.pincode)
