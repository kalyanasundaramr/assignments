
from pydantic import BaseModel

# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: Convert model to dictionary and JSON string. Here, the Student model is converted to a Python dictionary and a JSON string. 
# Learning: model_dump() returns a Python dictionary, while model_dump_json() returns a JSON string. These are Pydantic v2 methods.
class Student(BaseModel):
    id: int
    name: str
    course: str

student = Student(
    id=101,
    name="Manoj",
    course="Python"
)

# Convert to a Python dictionary
print(student.model_dump())

# Convert to a JSON string
print(student.model_dump_json(indent=2))
