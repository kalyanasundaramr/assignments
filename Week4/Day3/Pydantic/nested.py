
from pydantic import BaseModel

# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: Nested models allow for complex data structures. Here, the Person model contains an Address model as a field.
class Address(BaseModel):
    city: str
    pincode: str

class Person(BaseModel):
    name: str
    address: Address

person = Person(
    name="Meera",
    address={
        "city": "Chennai",
        "pincode": "600001"
    }
)

print("Name:", person.name)
print("City:", person.address.city)
print("Pincode:", person.address.pincode)
