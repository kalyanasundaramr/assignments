
from pydantic import BaseModel, ValidationError

# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: ValidationError is raised when the supplied data does not match the field types.
class User(BaseModel):
    name: str
    age: int

try:
    user = User(
        name="Kumar",
        age="hello"
    )
    print(user)

except ValidationError as e:
    print("Validation failed!")
    print(e)
