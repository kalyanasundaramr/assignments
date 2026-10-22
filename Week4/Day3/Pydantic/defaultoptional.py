
from pydantic import BaseModel

# Learning: BaseModel defines the fields and validates the supplied data.
# Learning: Default values fill in missing fields. Optional fields can be None. Here, salary is required, while department and bonus are not.
class Employee(BaseModel):
    name: str
    department: str = "IT"
    salary: float
    bonus: float | None = None

emp = Employee(
    name="Arun",
    salary=50000
)

print(emp)
print("Department:", emp.department)
print("Bonus:", emp.bonus)
