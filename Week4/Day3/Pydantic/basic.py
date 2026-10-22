
from pydantic import BaseModel

# Learning: BaseModel defines the fields and validates the supplied data.
class Student(BaseModel):
    id: int
    name: str
    course: str
    age: int

student = Student(
    id=101,
    name="Manoj",
    course="Python",
    age=25
)

print(student)
print("Name:", student.name)
print("Course:", student.course)

