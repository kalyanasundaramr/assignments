
from pydantic import BaseModel, Field, ValidationError

# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: Field constraints allow for validation of field values. Here, name must be between
    # 2 and 50 characters, price must be greater than 0, and quantity must be greater than or equal to 0. 
class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

try:
    product = Product(
        name="Laptop",
        price=999.99,
        quantity=5
    )
    print(product)

except ValidationError as e:
    print(e)
