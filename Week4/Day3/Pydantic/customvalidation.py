
from pydantic import BaseModel, field_validator
# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: Custom validation allows for additional checks on field values. Here, the email field is validated to ensure it contains an "@" symbol and a "." after the "@" symbol.
# Learning: field_validator lets you implement custom validation and normalize values. This is a simple demonstration, not a complete email validation standard.
class Customer(BaseModel):
    name: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()

        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email address")

        return value

customer = Customer(
    name="Manoj",
    email=" MANOJ@EXAMPLE.COM "
)

print(customer)
